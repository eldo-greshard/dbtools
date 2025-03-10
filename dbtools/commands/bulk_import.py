import subprocess
import sys
import os

def run_psql_command(pgservice, database, command):
    """Runs a PostgreSQL command using subprocess."""
    full_command = f'PGSERVICE={pgservice} psql -d {database} -c "{command}"'
    try:
        result = subprocess.run(full_command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing command: {command}\n{e.stderr}")

def bulk_import(pgservice, database, csv_dir):
    """Imports missing data from all CSV files in a directory into PostgreSQL."""
    
    # Ensure the directory exists
    if not os.path.exists(csv_dir):
        print(f"❌ Error: CSV directory '{csv_dir}' does not exist.")
        return

    # Process each CSV file in the given directory
    for csv_file in os.listdir(csv_dir):
        if not csv_file.endswith(".csv"):
            continue  # Skip non-CSV files
        
        csv_path = os.path.join(csv_dir, csv_file)

        # Extract target_table from the CSV file name (assuming 'table_name.csv' format)
        target_table = os.path.splitext(csv_file)[0]
        temp_table = f"tmp_{target_table}"  # Prefix temp table with "tmp_"

        print(f"\n🔄 Processing: {csv_file} → Target Table: {target_table} | Temp Table: {temp_table}")

        print("🔹 Creating temporary table...")
        run_psql_command(pgservice, database, f"CREATE TABLE {temp_table} AS TABLE {target_table} WITH NO DATA;")

        print(f"🔹 Importing data from {csv_path} into {temp_table}...")
        run_psql_command(pgservice, database, f"\\COPY {temp_table} FROM '{csv_path}' CSV HEADER;")

        print("🔹 Inserting data into main table...")
        run_psql_command(pgservice, database, f"""
            INSERT INTO {target_table}
            SELECT * FROM {temp_table}
            ON CONFLICT (id) DO NOTHING;
            DROP TABLE {temp_table};
        """)

        print(f"✅ Import completed for {csv_file}!\n")

    print("🎯 All CSV files processed successfully!")

def run(pg_service, database, csv_dir):
    # if len(sys.argv) < 4:
    #     print("\nUsage: dbtools import_missing_data <pg_service> <database> <csv_directory>")
    #     sys.exit(1)

    # pg_service = sys.argv[3]
    # database = sys.argv[5]
    # csv_dir = sys.argv[7]

    bulk_import(pg_service, database, csv_dir)
