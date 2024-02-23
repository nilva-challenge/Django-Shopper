#!/bin/bash

# Exit script in case of error
set -e

# Check the first argument to the script
case "$1" in
  runserver)
    # Wait for the DB to be ready
    echo "Waiting for PostgreSQL to start..."
    while ! nc -z db 5432; do
      sleep 0.1
    done
    echo "PostgreSQL started"

    # Apply database migrations
    echo "Applying database migrations..."
    python manage.py migrate --noinput

    # Collect static files
    echo "Collecting static files..."
    python manage.py collectstatic --noinput

    # Start Django app with uWSGI
    echo "Starting Django with uWSGI..."
    exec uwsgi --http :8000 --module prj.wsgi
    ;;


  bash)
    # Start Bash shell
    exec /bin/bash
    ;;

  *)
    # Default case or if no arguments provided
    echo "No valid argument provided. Running bash..."
    exec /bin/bash
    ;;
esac