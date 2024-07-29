#!/bin/sh

set -e

db_url="$DATABASE_URL"
shift
cmd="$@"

# Adiciona um atraso antes de tentar se conectar ao PostgreSQL
sleep 3

until PGPASSWORD=$(echo "$db_url" | sed -e 's,^.*://[^:]*:\([^@]*\)@.*, \1,') \
      PGUSER=$(echo "$db_url" | sed -e 's,^.*://\([^:]*\):.*,\1,') \
      PGHOST=$(echo "$db_url" | sed -e 's,^.*://[^@]*@\(.*\):.*,\1,') \
      PGPORT=$(echo "$db_url" | sed -e 's,^.*:\([0-9]*\)/.*,\1,') \
      PGDATABASE=$(echo "$db_url" | sed -e 's,^.*/\([^?]*\).*,\1,') \
      psql -h "$PGHOST" -U "$PGUSER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd