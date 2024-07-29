#!/bin/sh

set -e

db_url="$DATABASE_URL"
shift
cmd="$@"

PGPASSWORD=$(echo "$db_url" | sed -e 's,^.*://[^:]*:\([^@]*\)@.*, \1,')
PGUSER=$(echo "$db_url" | sed -e 's,^.*://\([^:]*\):.*,\1,')
PGHOST=$(echo "$db_url" | sed -e 's,^.*://[^@]*@\(.*\):[0-9]*/.*,\1,')
PGPORT=$(echo "$db_url" | sed -e 's,^.*://[^@]*@\([^:]*\):\([0-9]*\)/.*,\2,')
PGDATABASE=$(echo "$db_url" | sed -e 's,^.*/\([^?]*\).*,\1,')

echo "Trying to connect to PGHOST=$PGHOST, PGPORT=$PGPORT, PGUSER=$PGUSER, PGDATABASE=$PGDATABASE"

until PGPASSWORD=$PGPASSWORD \
      psql -h "$PGHOST" -U "$PGUSER" -p "$PGPORT" -d "$PGDATABASE" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
