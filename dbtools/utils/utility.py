import subprocess

def run_psql_command(pgservice, database, command):
    """Runs a PostgreSQL command using subprocess."""
    full_command = f'PGSERVICE={pgservice} psql -d {database} -c "{command}"'
    
    try:
        # Run the command and capture the output
        result = subprocess.run(full_command, shell=True, check=True, text=True, capture_output=True)
        
        # Check if the command is a SELECT query and return the output accordingly
        if command.strip().startswith("SELECT"):
            # If it's a SELECT query, process the output (result.stdout)
            # Split by lines, remove the first two lines (header and separator), and remove the row count line
            output_lines = result.stdout.strip().splitlines()[2:]  # Skip the header and separator lines
            filtered_lines = [line for line in output_lines if "rows" not in line]  # Remove lines containing 'rows'
            
            # Split by pipe (|) and strip spaces from each column name
            rows = [line.split('|') for line in filtered_lines]
            
            # Flatten and clean the column names by stripping extra spaces
            cleaned_columns = [col.strip() for row in rows for col in row if col.strip()]
            
            return cleaned_columns
        
        print(result.stdout)  # Print the command output
        return result  # Return the full result object for non-SELECT queries
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing command: {command}\n{e.stderr}")
        return None
    
def get_columns(pgservice, database, table_name):
    """
    Retrieves column names from a specified table in the database.
    """
    query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
    result = run_psql_command(pgservice, database, query)
    
    # Ensure the result is a list of strings (flatten if necessary)
    if result:
        # Flatten the result and return the list of column names
        return [column.strip() for column in result if column.strip()]
    return []

def get_missing_columns(pgservice, database, source_table, target_table):
    """
    Retrieves columns that are present in the target table but missing from the source table.
    """
    # Query to get the columns from both tables
    source_query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{source_table}'"
    target_query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{target_table}'"
    
    # Run the queries to get the columns for both tables
    source_columns = run_psql_command(pgservice, database, source_query)
    target_columns = run_psql_command(pgservice, database, target_query)
    
    if source_columns and target_columns:
        # Flatten the result and strip extra spaces from the columns
        source_columns = [col.strip() for col in source_columns if col.strip()]
        target_columns = [col.strip() for col in target_columns if col.strip()]
        
        # Find the columns that are in the target table but not in the source table (missing columns)
        missing_columns = [col for col in target_columns if col not in source_columns]
        return missing_columns
    return []


def alter_table_for_missing_columns(pgservice, database, temp_table, target_columns, csv_columns):
    """
    Alters the temporary table to ensure that columns present in the target table but missing in the CSV
    are set to accept NULL values during the COPY operation.
    """
    # Find columns in the target table that are missing in the CSV
    missing_columns = [col for col in target_columns if col not in csv_columns]
    
    # Alter the table to set the missing columns' default value to NULL
    for column in missing_columns:
        print(f"🔹 Altering column {column} in {temp_table} to accept NULL")
        run_psql_command(pgservice, database, f"ALTER TABLE {temp_table} ALTER COLUMN {column} SET DEFAULT NULL;")
