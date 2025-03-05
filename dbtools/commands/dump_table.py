import csv
import os

def dump_table(reference_db, csv_file, output_dump_file):
    """Generates a SQL dump script to restore missing data."""
    
    # Ensure output file has the correct extension
    if not output_dump_file.endswith(".sql"):
        output_dump_file += ".sql"

    # Validate CSV file
    if not csv_file.endswith(".csv") or not os.path.exists(csv_file):
        print(f"❌ Error: Invalid or missing CSV file '{csv_file}'.")
        return

    # Read CSV and group missing IDs by table
    missing_data = {}
    try:
        with open(csv_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)

            # Ensure required columns exist
            required_columns = {"table_name", "id"}
            if not required_columns.issubset(reader.fieldnames):
                print("❌ Error: CSV file must contain 'table_name' and 'id' columns.")
                return

            for row in reader:
                table = row["table_name"]
                missing_id = row["id"]

                if table not in missing_data:
                    missing_data[table] = set()

                missing_data[table].add(missing_id)
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return

    if not missing_data:
        print("✅ No missing data found.")
        return

    # Generate SQL dump script
    with open(output_dump_file, mode="w") as dump_file:
        dump_file.write(f"-- PostgreSQL dump script to restore missing data from {reference_db}\n\n")

        for table, ids in missing_data.items():
            id_list = ", ".join(map(str, ids))
            dump_file.write(f"-- Dump data for table: {table}\n")
            dump_file.write(
                f"COPY (SELECT * FROM {table} WHERE id IN ({id_list})) TO 'missing_{table}.csv' CSV HEADER;\n\n"
            )

    print(f"\n✅ Dump script generated: {output_dump_file}")
    print(f"🎯 To execute it, run: psql -U your_username -d {reference_db} -f {output_dump_file}")
