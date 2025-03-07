import sys
import argparse
from dbtools.const import BANNER, DESCRIPTION
from dbtools.utils import find_best_command
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
        ("output_dump_file", "Output dump file")
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
        user_input = input("\n🔹 Enter a number OR describe your action: ").strip().lower()

        if user_input == "9":
            print("✅ Exiting... Goodbye!")
            sys.exit(0)

        # If user inputs a number, use the standard COMMANDS dictionary
        if user_input in COMMANDS:
            command_key = user_input
        else:
            # Use AI to determine the best command match
            command_key = find_best_command(user_input)
            if not command_key:
                print("❌ Could not understand your request. Please select a valid option.")
                continue

        command_name, command_module, params = COMMANDS[command_key]
        print(f"\n🚀 Executing: {command_name}\n")
        
        # Collect arguments interactively
        args = {}
        for arg, desc in params:
            args[arg] = get_user_input(desc)
        
        # Run the command
        command_module.run(**args)

if __name__ == "__main__":
    main()
