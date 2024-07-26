#!/bin/sh

set -e

host="$1"
shift
cmd="$@"

until PGPASSWORD=$(echo "$DATABASE_URL" | sed -e 's,^.*://[^:]*:\([^@]*\)@.*, \1,') \
      PGUSER=$(echo "$DATABASE_URL" | sed -e 's,^.*://\([^:]*\):.*,\1,') \
      PGHOST=$(echo "$DATABASE_URL" | sed -e 's,^.*://[^@]*@\(.*\):.*,\1,') \
      PGPORT=$(echo "$DATABASE_URL" | sed -e 's,^.*:\([0-9]*\)/.*,\1,') \
      PGDATABASE=$(echo "$DATABASE_URL" | sed -e 's,^.*/\([^?]*\).*,\1,') \
      psql -h "$PGHOST" -U "$PGUSER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd