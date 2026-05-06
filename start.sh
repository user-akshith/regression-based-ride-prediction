#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn Uber_fare.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers 2 \
  --timeout 120
