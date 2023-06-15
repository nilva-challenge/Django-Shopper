#!/bin/bash
set -e

# There are some times database is not ready yet!
# We'll check if database is ready and we can connect to it
# then the rest of the code run as well.
env >/.env

echo "Waiting for database..."
echo DB_NAME: ${DB_NAME}
echo DB_HOST: ${DB_HOST}
echo DB_PORT: ${DB_PORT}
echo "Connected to database."

if [ ${MIGRATE} == 'True' ]; then
  echo "Start MIGRATE"
  python manage.py migrate --no-input
  status=$?
  if [ $status -ne 0 ]; then
    echo "Failed to migrate database: $status"
    exit $status
  fi
fi

if [ ${COLLECT_STATIC} == 'True' ]; then
  python manage.py collectstatic --no-input --clear
  status=$?
  if [ $status -ne 0 ]; then
    echo "Failed to collect staticfiles: $status"
    exit $status
  fi
fi

gunicorn

