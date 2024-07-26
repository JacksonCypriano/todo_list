#!/bin/bash
set -e

echo "host all all 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"
echo "listen_addresses='*'" >> "$PGDATA/postgresql.conf"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
  DO \$\$ 
  BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'tasks') THEN
      CREATE DATABASE tasks;
    END IF;
  END
  \$\$;
EOSQL