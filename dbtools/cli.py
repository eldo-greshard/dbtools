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

    subparsers = parser.add_subparsers(dest="command", help="Available commands",required=True)

    # Command: auto_export_compare_table
    subparsers.add_parser("auto_export_compare_table", help="Automatically compare all tables and export results.")

    # Command: compare_db
    parser_compare_db  = subparsers.add_parser("compare_db", help="Compare entire databases.")
    parser_compare_db.add_argument("--pg_service", required=True, help="PostgreSQL service name")
    parser_compare_db.add_argument("--db1", required=True, help="First database name")
    parser_compare_db.add_argument("--db2", required=True, help="Second database name")
    parser_compare_db.add_argument("--csvoutput", required=True, help="Output File extension *.csv")

    # Command: compare_selected_table
    parser_compare_selected_table = subparsers.add_parser("compare_selected_table", help="Compare specific tables between two databases.")
    """Entry point for comparing selected tables between two PostgreSQL databases."""
    parser_compare_selected_table.add_argument("--pgservice", required=True, help="PostgreSQL service name")
    
    # Command: dump_table
    parser_dump_table = subparsers.add_parser("dump_table", help="Dump specific tables from a database.")
    parser_dump_table.add_argument("--reference_db", required=True, help="Reference database")
    parser_dump_table.add_argument("--csv_file", required=True, help="CSV File")
    parser_dump_table.add_argument("--output_dump_file", required=True, help="Output Dump File")

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
