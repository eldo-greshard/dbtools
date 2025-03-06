import sys
import psycopg2
import csv
import argparse

def get_databases(pg_service):
    """Fetch available databases."""
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

def connect_to_db(pg_service, db_name):
    """Connect to a PostgreSQL database."""
    try:
        return psycopg2.connect(service=pg_service, dbname=db_name)
    except Exception as e:
        print(f"❌ Error connecting to {db_name}: {e}")
        return None

def get_tables(cursor):
    """Fetch all public tables in a database."""
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    return {row[0] for row in cursor.fetchall()}

def get_table_data(cursor, table_name):
    """Fetch table data for comparison."""
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        return set(cursor.fetchall())  # Convert to set for easy comparison
    except Exception as e:
        print(f"⚠️ Error fetching data from {table_name}: {e}")
        return set()

def compare_selected_tables(pg_service, db1, db2, selected_tables):
    """Compare selected tables between two databases."""
    print(f"\n🔍 Comparing databases: {db1} vs {db2}")

    conn1 = connect_to_db(pg_service, db1)
    conn2 = connect_to_db(pg_service, db2)

    if not conn1 or not conn2:
        return

    cur1 = conn1.cursor()
    cur2 = conn2.cursor()

    for table in selected_tables:
        print(f"🔍 Comparing data for table: {table}")

        data_db1 = get_table_data(cur1, table)
        data_db2 = get_table_data(cur2, table)

        missing_in_db2 = data_db1 - data_db2
        # missing_in_db1 = data_db2 - data_db1

        differences = []

        for row in missing_in_db2:
            differences.append({"id": row[0], "database_name": db2, "table_name": table, "note": "Missing in db2"})

        # for row in missing_in_db1:
        #     differences.append({"id": row[0], "database_name": db1, "table_name": table, "note": "Missing in db1"})

        # Save differences to a CSV file specific to the table
        output_file = f"{table}_differences.csv"
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
    

def run():
    if len(sys.argv) < 3:
        print("\nUsage: dbtools compare_selected_tables <pg_service>")
        sys.exit(1)
        
    pg_service = sys.argv[3]
    

    # Fetch available databases
    databases = get_databases(pg_service)
    if len(databases) < 2:
        print("❌ At least two databases are required for comparison.")
        return
    
    print("\n📌 Available databases:")
    for db in databases:
        print(f"  - {db}")

    db1 = input("\nEnter the first database name: ").strip()
    db2 = input("Enter the second database name: ").strip()

    if db1 not in databases or db2 not in databases:
        print("❌ Invalid database selection.")
        return

    selected_tables = input("\nEnter table names to compare (comma-separated) or 'all' for all tables: ").strip()
    
    if selected_tables.lower() == "all":
        from dbtools.commands.compare_selected_table import connect_to_db, get_tables
        conn = connect_to_db(pg_service, db1)
        if conn:
            cur = conn.cursor()
            selected_tables = get_tables(cur)
            conn.close()
        else:
            return
    else:
        selected_tables = [t.strip() for t in selected_tables.split(",") if t.strip()]

    if not selected_tables:
        print("❌ No valid tables selected.")
        return

    compare_selected_tables(pg_service, db1, db2, selected_tables)
