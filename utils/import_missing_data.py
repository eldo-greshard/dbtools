import subprocess

def run_psql_command(pgservice, database, command):
    """Runs a PostgreSQL command using subprocess."""
    full_command = f'PGSERVICE={pgservice} psql -d {database} -c "{command}"'
    try:
        result = subprocess.run(full_command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing command: {command}\n{e.stderr}")

def import_missing_data(pgservice, database, csv_file, temp_table, target_table):
    """Imports missing data from CSV into PostgreSQL."""
    
    print("🔹 Creating temporary table...")
    run_psql_command(pgservice, database, f"CREATE TABLE {temp_table} AS TABLE {target_table} WITH NO DATA;")

    print(f"🔹 Importing data from {csv_file}...")
    run_psql_command(pgservice, database, f"\\COPY {temp_table} FROM '{csv_file}' CSV HEADER;")

    print("🔹 Inserting data into main table...")
    run_psql_command(pgservice, database, f"""
        INSERT INTO {target_table}
        SELECT * FROM {temp_table}
        ON CONFLICT (path) DO NOTHING;
        DROP TABLE {temp_table};
    """)

    print("✅ Import process completed successfully!")
