import psycopg2
import csv
import sys
import os

# Default PostgreSQL Service Name (can be overridden via command-line)
DEFAULT_PG_SERVICE = "set-your-pg-service"

# Function to get available databases
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

# Function to fetch tables from a database
def get_tables(cursor):
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    return {row[0] for row in cursor.fetchall()}

# Function to fetch table data
def get_table_data(cursor, table_name):
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        return set(cursor.fetchall())  # Convert to set for easy comparison
    except Exception as e:
        print(f"⚠️ Error fetching data from {table_name}: {e}")
        return set()

# Function to compare tables between two databases
def compare_tables(db1, db2, output_file, pg_service):
    print(f"\n🔍 Comparing databases: {db1} vs {db2}")

    conn1 = connect_to_db(db1, pg_service)
    conn2 = connect_to_db(db2, pg_service)

    if not conn1 or not conn2:
        return

    cur1 = conn1.cursor()
    cur2 = conn2.cursor()

    tables_db1 = get_tables(cur1)
    tables_db2 = get_tables(cur2)

    all_tables = tables_db1 | tables_db2  # Union of all tables
    differences = []

    for table in all_tables:
        if table not in tables_db1:
            print(f"⚠️ Table '{table}' exists in {db2} but not in {db1}")
            differences.append({"id": "N/A", "database_name": db1, "table_name": table, "note": "Missing table"})
            continue
        if table not in tables_db2:
            print(f"⚠️ Table '{table}' exists in {db1} but not in {db2}")
            differences.append({"id": "N/A", "database_name": db2, "table_name": table, "note": "Missing table"})
            continue

        print(f"🔍 Comparing data for table: {table}")

        data_db1 = get_table_data(cur1, table)
        data_db2 = get_table_data(cur2, table)

        missing_in_db2 = data_db1 - data_db2
        # missing_in_db1 = data_db2 - data_db1

        for row in missing_in_db2:
            differences.append({"id": row[0], "database_name": db2, "table_name": table, "note": "Missing in db2"})

        # for row in missing_in_db1:
        #     differences.append({"id": row[0], "database_name": db1, "table_name": table, "note": "Missing in db1"})

    # Save differences to CSV
    if differences:
        with open(output_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "database_name", "table_name", "note"])
            writer.writeheader()
            writer.writerows(differences)
        print(f"\n✅ Differences saved to {output_file}")
    else:
        print("\n✅ No differences found.")

    cur1.close()
    cur2.close()
    conn1.close()
    conn2.close()

# Entry point for CLI integration
def run():
    if len(sys.argv) < 5:
        print("\nUsage: dbtools compare_db <pg_service> <db1> <db2> <output_file>")
        sys.exit(1)

    pg_service = sys.argv[2]
    db1 = sys.argv[3]
    db2 = sys.argv[4]
    output_file = sys.argv[5]

    databases = get_databases(pg_service)

    if db1 not in databases or db2 not in databases:
        print("❌ Invalid database selection. Please choose from the available list.")
    elif db1 == db2:
        print("❌ Cannot compare a database with itself.")
    else:
        compare_tables(db1, db2, output_file, pg_service)
