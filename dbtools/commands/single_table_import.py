import subprocess
import sys

def run_psql_command(pgservice, database, command):
    """Runs a PostgreSQL command using subprocess."""
    full_command = f'PGSERVICE={pgservice} psql -d {database} -c "{command}"'
    try:
        result = subprocess.run(full_command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing command: {command}\n{e.stderr}")

def single_table_import(pgservice, database, csv_file, temp_table, target_table, conflict_column):
    """Imports missing data from CSV into PostgreSQL."""
    
    print("🔹 Creating temporary table...")
    run_psql_command(pgservice, database, f"CREATE TABLE {temp_table} AS TABLE {target_table} WITH NO DATA;")

    print(f"🔹 Importing data from {csv_file}...")
    run_psql_command(pgservice, database, f"\\COPY {temp_table} FROM '{csv_file}' CSV HEADER;")

    print("🔹 Inserting data into main table...")
    run_psql_command(pgservice, database, f"""
        INSERT INTO {target_table}
        SELECT * FROM {temp_table}
        ON CONFLICT ({conflict_column}) DO NOTHING;
    """)

    print("🔹 Dropping temporary table...")
    run_psql_command(pgservice, database, f"DROP TABLE {temp_table};")

    print("✅ Import process completed successfully!")

def run():
    pg_service = sys.argv[3]
    database = sys.argv[5]
    csv_file = sys.argv[7]
    temp_table = sys.argv[9]
    target_table = sys.argv[11]
    conflict_column = sys.argv[13]

    single_table_import(pg_service, database, csv_file, temp_table, target_table, conflict_column)