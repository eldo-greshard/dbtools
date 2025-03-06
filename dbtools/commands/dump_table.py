import csv
import os
import sys

def dump_table(reference_db, csv_dir, output_dir):
    """Generates SQL dump scripts to restore missing data from all CSV files in a directory."""
    
    # Ensure the input CSV directory exists
    if not os.path.exists(csv_dir):
        print(f"❌ Error: CSV directory '{csv_dir}' does not exist.")
        return

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each CSV file in the given directory
    for csv_file in os.listdir(csv_dir):
        
        if not csv_file.endswith(".csv"):
            continue  # Skip non-CSV files
        
        csv_path = os.path.join(csv_dir, csv_file)
        output_dump_file = os.path.join(output_dir, f"{os.path.splitext(csv_file)[0]}.sql")

        print(f"🔄 Processing: {csv_file} → {output_dump_file}")

        missing_data = {}

        try:
            with open(csv_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)

                # Ensure required columns exist
                required_columns = {"table_name", "id"}
                if not required_columns.issubset(reader.fieldnames):
                    print(f"⚠️ Skipping {csv_file}: Missing required columns {required_columns}.")
                    continue

                for row in reader:
                    table = row["table_name"]
                    missing_id = row["id"]

                    if table not in missing_data:
                        missing_data[table] = set()

                    missing_data[table].add(missing_id)
        except Exception as e:
            print(f"❌ Error reading {csv_file}: {e}")
            continue

        if not missing_data:
            print(f"✅ No missing data found in {csv_file}.")
            continue

        # Generate SQL dump script
        with open(output_dump_file, mode="w") as dump_file:
            dump_file.write(f"-- PostgreSQL dump script to restore missing data from {reference_db}\n\n")

            for table, ids in missing_data.items():
                id_list = ", ".join(map(str, ids))
                dump_file.write(f"-- Dump data for table: {table}\n")
                dump_file.write(
                    f"COPY (SELECT * FROM {table} WHERE id IN ({id_list})) TO 'missing_{table}.csv' CSV HEADER;\n\n"
                )

        print(f"✅ Dump script generated: {output_dump_file}")

    print("\n🎯 To execute the dump scripts, run:")
    print(f"psql -U your_username -d {reference_db} -f <path_to_sql_script>")

def run():
    if len(sys.argv) < 5:
        print("\nUsage: dbtools dump_table <pg_service> <csv_directory> <output_directory>")
        sys.exit(1)

    reference_db = sys.argv[3]
    csv_dir = sys.argv[5]
    output_dir = sys.argv[7]

    dump_table(reference_db, csv_dir, output_dir)
