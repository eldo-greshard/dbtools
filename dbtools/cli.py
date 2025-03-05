import argparse
import sys
from dbtools.commands import (
    auto_export_compare_table,
    compare_db,
    compare_selected_table,
    dump_table,
    import_missing_data
)

def main():
    parser = argparse.ArgumentParser(prog="dbtools", description="Database Tools CLI")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: auto_export_compare_table
    subparsers.add_parser("auto_export_compare_table", help="Automatically compare all tables and export results.")

    # Command: compare_db
    subparsers.add_parser("compare_db", help="Compare entire databases.")

    # Command: compare_selected_table
    subparsers.add_parser("compare_selected_table", help="Compare specific tables between two databases.")

    # Command: dump_table
    subparsers.add_parser("dump_table", help="Dump specific tables from a database.")

    # Command: import_missing_data
    subparsers.add_parser("import_missing_data", help="Import missing data into a database.")

    args = parser.parse_args()

    if args.command == "auto_export_compare_table":
        auto_export_compare_table.run()
    elif args.command == "compare_db":
        compare_db.run()
    elif args.command == "compare_selected_table":
        compare_selected_table.run()
    elif args.command == "dump_table":
        dump_table.run()
    elif args.command == "import_missing_data":
        import_missing_data.run()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
