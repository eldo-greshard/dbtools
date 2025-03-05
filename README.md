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
