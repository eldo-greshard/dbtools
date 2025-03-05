import psycopg2
import csv
import os
import sys

# Function to get PostgreSQL Service Name from user
def get_pg_service():
    return input("Enter the PostgreSQL service name: ").strip()

# Function to get the output directory for CSV files
def get_output_dir():
    output_dir = input("Enter the output directory for CSV files: ").strip()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create directory if it doesn't exist
        print(f"📁 Created output directory: {output_dir}")
    return output_dir

# Fetch available databases
def get_databases(pg_service):
    try:
        conn = psycopg2.connect(service=pg_service, dbname="postgres")
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false")
        databases = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return databases
    except Exception as e:
        print(f"❌ Error fetching databases: {e}")
        return []

# Function to connect to a database
def connect_to_db(db_name, pg_service):
    try:
        return psycopg2.connect(service=pg_service, dbname=db_name)
    except Exception as e:
        print(f"❌ Error connecting to {db_name}: {e}")
        return None

# Fetch tables from a database
def get_tables(cursor):
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    return {row[0] for row in cursor.fetchall()}

# Fetch table data
def get_table_data(cursor, table_name):
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        return set(cursor.fetchall())  # Convert to set for easy comparison
    except Exception as e:
        print(f"⚠️ Error fetching data from {table_name}: {e}")
        return set()

# Compare tables between two databases automatically
def compare_all_tables(db1, db2, common_tables, output_dir, pg_service):
    print(f"\n🔍 Comparing all common tables between databases: {db1} vs {db2}")

    conn1 = connect_to_db(db1, pg_service)
    conn2 = connect_to_db(db2, pg_service)

    if not conn1 or not conn2:
        return

    cur1 = conn1.cursor()
    cur2 = conn2.cursor()

    for table in common_tables:
        print(f"🔍 Comparing data for table: {table}")

        data_db1 = get_table_data(cur1, table)
        data_db2 = get_table_data(cur2, table)

        missing_in_db2 = data_db1 - data_db2
        missing_in_db1 = data_db2 - data_db1

        differences = []

        for row in missing_in_db2:
            differences.append({"id": row[0], "database_name": db2, "table_name": table, "note": "Missing in db2"})

        for row in missing_in_db1:
            differences.append({"id": row[0], "database_name": db1, "table_name": table, "note": "Missing in db1"})

        # Save differences to a CSV file specific to the table inside the user-defined directory
        output_file = os.path.join(output_dir, f"{table}_differences.csv")
        if differences:
            with open(output_file, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["id", "database_name", "table_name", "note"])
                writer.writeheader()
                writer.writerows(differences)
            print(f"✅ Differences for table '{table}' saved to {output_file}")
        else:
            print(f"✅ No differences found for table '{table}'.")

    cur1.close()
    cur2.close()
    conn1.close()
    conn2.close()

# Main function
def run():
    if len(sys.argv) < 5:
        print("\nUsage: dbtools auto_export_compare_table <pg_service> <db1> <db2> <output_dir>")
        sys.exit(1)

    pg_service = sys.argv[2]
    db1 = sys.argv[3]
    db2 = sys.argv[4]
    output_dir = sys.argv[5]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created output directory: {output_dir}")

    databases = get_databases(pg_service)

    if db1 not in databases or db2 not in databases:
        print("❌ Invalid database selection. Please choose from the available list.")
        sys.exit(1)
    elif db1 == db2:
        print("❌ Cannot compare a database with itself.")
        sys.exit(1)

    # Get tables in both databases
    conn1 = connect_to_db(db1, pg_service)
    conn2 = connect_to_db(db2, pg_service)

    if not conn1 or not conn2:
        sys.exit(1)

    cur1 = conn1.cursor()
    cur2 = conn2.cursor()

    tables_db1 = get_tables(cur1)
    tables_db2 = get_tables(cur2)

    common_tables = tables_db1 & tables_db2  # Only tables existing in both databases

    cur1.close()
    cur2.close()
    conn1.close()
    conn2.close()

    if not common_tables:
        print("❌ No common tables found between the databases.")
        sys.exit(1)

    print(f"\n📌 {len(common_tables)} common tables detected. Comparing all tables...")

    compare_all_tables(db1, db2, common_tables, output_dir, pg_service)
