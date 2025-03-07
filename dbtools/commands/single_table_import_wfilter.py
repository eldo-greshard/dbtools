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

def get_filter_values(filter_csv, filter_column):
    """Reads the filter CSV file and extracts unique values from the specified filter column."""
    try:
        df = pd.read_csv(filter_csv)
        if filter_column not in df.columns:
            raise ValueError(f"Filter column '{filter_column}' not found in {filter_csv}.")
        return df[filter_column].dropna().unique()
    except Exception as e:
        print(f"❌ Error reading filter file: {e}")
        sys.exit(1)

def single_table_import_wfilter(pgservice, database, csv_file, temp_table, target_table, filter_csv, filter_column, conflict_column):
    """Imports filtered data from CSV into PostgreSQL."""
    
    print("🔹 Creating temporary table...")
    run_psql_command(pgservice, database, f"CREATE TABLE {temp_table} AS TABLE {target_table} WITH NO DATA;")

    print(f"🔹 Importing data from {csv_file}...")
    run_psql_command(pgservice, database, f"\\COPY {temp_table} FROM '{csv_file}' CSV HEADER;")

    print("🔹 Extracting filter values...")
    filter_values = get_filter_values(filter_csv, filter_column)
    filter_values_str = ','.join([f"'{value}'" for value in filter_values])

    print("🔹 Inserting filtered data into main table...")
    run_psql_command(pgservice, database, f"""
        INSERT INTO {target_table}
        SELECT * FROM {temp_table}
        WHERE {filter_column} IN ({filter_values_str})
        ON CONFLICT ({conflict_column}) DO NOTHING;
    """)

    print("🔹 Dropping temporary table...")
    run_psql_command(pgservice, database, f"DROP TABLE {temp_table};")

    print("✅ Import process completed successfully!")

def run():
    if len(sys.argv) < 13:
        print("❌ Usage: script.py --pgservice <pg_service> --database <database> --csv <csv_file> --temp-table <temp_table> --target-table <target_table> --filter-csv <filter_csv> --filter-column <filter_column>")
        sys.exit(1)

    pg_service = sys.argv[3]
    database = sys.argv[5]
    csv_file = sys.argv[7]
    temp_table = sys.argv[9]
    target_table = sys.argv[11]
    filter_csv = sys.argv[13]
    filter_column = sys.argv[15]
    conflict_column = sys.argv[17]

    single_table_import_wfilter(pg_service, database, csv_file, temp_table, target_table, filter_csv, filter_column, conflict_column)

if __name__ == "__main__":
    run()
