import os
import sys
import subprocess

def execute_sql_script(pgservice, database, sql_script_path):
    """Executes a single SQL dump script using psql with PGSERVICE."""
    if not os.path.exists(sql_script_path) or not sql_script_path.endswith(".sql"):
        print(f"❌ Skipping invalid SQL script: {sql_script_path}")
        return

    print(f"🔹 Executing: {sql_script_path}")
    command = f'PGSERVICE={pgservice} psql -d {database} -f "{sql_script_path}"'
    
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
        print(f"✅ Successfully executed: {sql_script_path}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing {sql_script_path}:\n{e.stderr}\n")

def execute_dump_scripts(pgservice, database, scripts_dir):
    """Executes all SQL dump scripts in the specified directory."""
    
    if not os.path.exists(scripts_dir):
        print(f"❌ Error: The directory '{scripts_dir}' does not exist.")
        return

    sql_files = sorted([f for f in os.listdir(scripts_dir) if f.endswith(".sql")])

    if not sql_files:
        print("✅ No SQL scripts found to execute.")
        return

    print(f"\n📂 Found {len(sql_files)} SQL scripts in '{scripts_dir}'.\n")

    for sql_file in sql_files:
        sql_script_path = os.path.join(scripts_dir, sql_file)
        execute_sql_script(pgservice, database, sql_script_path)

    print("🎯 All SQL scripts executed successfully!")

def run():
    if len(sys.argv) < 4:
        print("\nUsage: dbtools execute_dump_scripts <pg_service> <database> <scripts_directory>")
        sys.exit(1)

    pg_service = sys.argv[3]
    database = sys.argv[5]
    scripts_dir = sys.argv[7]

    execute_dump_scripts(pg_service, database, scripts_dir)
