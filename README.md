# Postgresql DBTools
```
╔════════════════════════════════════════════════╗
║      🛠️  Database Tools CLI - v1.0 🛠️         ║
║         Efficient PostgreSQL Management        ║
╚════════════════════════════════════════════════╝

Welcome to Database Tools CLI!
This tool helps you manage, compare, and import/export PostgreSQL database data efficiently.

📌 Features:
✔ Compare entire databases or selected tables
✔ Export differences as CSV files
✔ Dump tables and restore missing data
✔ Execute SQL dump scripts
✔ Support for PostgreSQL service-based authentication (.pg_service.conf)

👉 Select an option from the menu to proceed.

==================================================
📌 Available Commands:
  1. Auto Export Compare Table
  2. Compare Databases
  3. Compare Selected Table
  4. Dump Table
  5. Bulk Import
  6. Single Table Import
  7. Single Table Import with Filter
  8. Execute Dump Script
  9. ❌ Exit
==================================================

🔹 Select an option (1-9): 

```

## Prerequisit

1. Install postgresql database
```
# Add Postgresql GPG Key

$ curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg

$ echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
```
```
# install postgresql
$ sudo apt install postgresql postgresql-contrib libpq-dev
```

2. Create postgreSQL service name (configured in ~/.pg_service.conf)
```
$ touch .pg_service.conf
$ nano .pg_service.config 
```

copy and paste this into .pg_service.config
```
[pg_service_name]
host=your-psql-host
port=your-psql-port
user=your-psql-user
password=your-psql-password
```
