import subprocess

def run_psql_command(pgservice, database, command):
    """Runs a PostgreSQL command using subprocess."""
    full_command = f'PGSERVICE={pgservice} psql -d {database} -c "{command}"'
    try:
        result = subprocess.run(full_command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing command: {command}\n{e.stderr}")

def get_columns(pgservice, database, table_name):
    """
    Retrieves column names from a specified table in the database.
    """
    query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
    result = run_psql_command(pgservice, database, query)
    return [row[0] for row in result]
