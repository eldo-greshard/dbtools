import sys
import argparse
from dbtools.commands import (
    auto_export_compare_table,
    bulk_import,
    compare_db,
    compare_selected_table,
    dump_table,
    execute_dump_script,
    single_table_import,
    single_table_import_wfilter
)

BANNER = """
╔════════════════════════════════════════════════╗
║      🛠️  Database Tools CLI - v1.0 🛠️         ║
║         Efficient PostgreSQL Management        ║
╚════════════════════════════════════════════════╝
"""

DESCRIPTION = """
Welcome to Database Tools CLI!
This tool helps you manage, compare, and import/export PostgreSQL database data efficiently.

📌 Features:
✔ Compare entire databases or selected tables
✔ Export differences as CSV files
✔ Dump tables and restore missing data
✔ Execute SQL dump scripts
✔ Support for PostgreSQL service-based authentication (.pg_service.conf)

👉 Select an option from the menu to proceed.
"""

COMMANDS = {
    "1": ("Auto Export Compare Table", auto_export_compare_table, [
        ("pg_service", "PostgreSQL service name"),
        ("db1", "First database name"),
        ("db2", "Second database name"),
        ("output_directory", "Output directory")
    ]),
    "2": ("Compare Databases", compare_db, [
        ("pg_service", "PostgreSQL service name"),
        ("db1", "First database name"),
        ("db2", "Second database name"),
        ("csvoutput", "Output CSV file path")
    ]),
    "3": ("Compare Selected Table", compare_selected_table, [
        ("pgservice", "PostgreSQL service name")
    ]),
    "4": ("Dump Table", dump_table, [
        ("reference_db", "Reference database"),
        ("csv_file", "CSV file"),
        ("output_dump_file", "Output dump file"),
        ("output_data_dir", "Output data directory")
    ]),
    "5": ("Bulk Import", bulk_import, [
        ("pg_service", "PostgreSQL service name"),
        ("database", "Target database"),
        ("csv_dir", "Directory containing CSV files")
    ]),
    "6": ("Single Table Import", single_table_import, [
        ("pg_service", "PostgreSQL service name"),
        ("database", "Target database"),
        ("csv_file", "CSV file"),
        ("temp_table", "Temporary table name"),
        ("target_table", "Target table name"),
        ("conflict_column", "Conflict column")
    ]),
    "7": ("Single Table Import with Filter", single_table_import_wfilter, [
        ("pg_service", "PostgreSQL service name"),
        ("database", "Target database"),
        ("csv_file", "CSV file"),
        ("temp_table", "Temporary table name"),
        ("target_table", "Target table name"),
        ("filter_csv", "Filter CSV file"),
        ("filter_column", "Filter column"),
        ("conflict_column", "Conflict column")
    ]),
    "8": ("Execute Dump Script", execute_dump_script, [
        ("pg_service", "PostgreSQL service name"),
        ("database", "Target database"),
        ("scripts_directory", "SQL scripts directory")
    ])
}

def get_user_input(prompt):
    """ Helper function to get user input with a prompt """
    return input(f"{prompt}: ").strip()

def display_menu():
    """ Display the command menu """
    print("\n" + "="*50)
    print("📌 Available Commands:")
    for key, (description, _, _) in COMMANDS.items():
        print(f"  {key}. {description}")
    print("  9. ❌ Exit")
    print("="*50)

def main():
    print(BANNER)
    print(DESCRIPTION)

    while True:
        display_menu()
        choice = input("\n🔹 Select an option (1-9): ").strip()

        if choice == "9":
            print("✅ Exiting... Goodbye!")
            sys.exit(0)

        if choice in COMMANDS:
            command_name, command_module, params = COMMANDS[choice]
            print(f"\n🚀 Executing: {command_name}\n")
            
            # Collect arguments interactively
            args = {}
            for arg, desc in params:
                args[arg] = get_user_input(desc)
            
            # Run the command
            command_module.run(**args)
        else:
            print("❌ Invalid option. Please choose a valid number.")

if __name__ == "__main__":
    main()
