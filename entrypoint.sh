#!/bin/sh


set -e

echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$POSTGRES_USER"
do
  sleep 1
done
echo "PostgreSQL is ready!"

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"