
import csv
import sys
import pandas as pd

from dbtools.utils.utility import alter_table_for_missing_columns, get_columns, get_missing_columns, run_psql_command


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
    print(f""" Execute : 
        CREATE TABLE {temp_table} AS TABLE {target_table} WITH NO DATA;
    """)
    print("-----------------------------------")
    run_psql_command(pgservice, database, f"CREATE TABLE {temp_table} AS TABLE {target_table} WITH NO DATA;")

    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        csv_header = next(csv_reader)  # Get the first row (header) of the CSV
    
    # Ensure that the CSV header contains only columns that exist in the target table
    # Filter out any CSV columns that do not exist in the target table
    valid_columns = [col for col in csv_header]
    
    # If there are no valid columns to copy, print an error and return
    if not valid_columns:
        print("❌ No matching columns between the CSV and the target table.")
        return

    # Construct the COPY command dynamically using valid columns
    columns_str = ", ".join(valid_columns)

    print(f"🔹 Importing data from {csv_file}...")
    print(f""" Execute : 
        \\COPY {temp_table} FROM '{csv_file}' CSV HEADER;
    """)
    print("-----------------------------------")
    run_psql_command(pgservice, database, f"\\COPY {temp_table} ({columns_str}) FROM '{csv_file}' CSV HEADER;")

    print("🔹 Extracting filter values...")
    filter_values = get_filter_values(filter_csv, filter_column)
    filter_values_str = ','.join([f"'{value}'" for value in filter_values])

    print("🔹 Inserting filtered data into main table...")
    print(f""" Execute : 
        INSERT INTO {target_table}
        SELECT * FROM {temp_table}
        WHERE {filter_column} IN ({filter_values_str})
        ON CONFLICT ({conflict_column}) DO NOTHING;
    """)
    print("-----------------------------------")
    run_psql_command(pgservice, database, f"""
        INSERT INTO {target_table}
        SELECT * FROM {temp_table}
        WHERE {filter_column} IN ({filter_values_str})
        ON CONFLICT ({conflict_column}) DO NOTHING;
    """)

    print("🔹 Dropping temporary table...")
    run_psql_command(pgservice, database, f"DROP TABLE {temp_table};")

    print("✅ Import process completed successfully!")

def run(pg_service, database, csv_file, temp_table, target_table, filter_csv, filter_column, conflict_column,):
    # if len(sys.argv) < 13:
    #     print("❌ Usage: script.py --pgservice <pg_service> --database <database> --csv <csv_file> --temp-table <temp_table> --target-table <target_table> --filter-csv <filter_csv> --filter-column <filter_column>")
    #     sys.exit(1)

    # pg_service = sys.argv[3]
    # database = sys.argv[5]
    # csv_file = sys.argv[7]
    # temp_table = sys.argv[9]
    # target_table = sys.argv[11]
    # filter_csv = sys.argv[13]
    # filter_column = sys.argv[15]
    # conflict_column = sys.argv[17]

    single_table_import_wfilter(pg_service, database, csv_file, temp_table, target_table, filter_csv, filter_column, conflict_column)

if __name__ == "__main__":
    run()
