#!/bin/sh
set -eu

cd /app

python manage.py migrate --noinput
python manage.py seed_catalog --prune

exec daphne \
  --bind 0.0.0.0 \
  --port 8000 \
  --proxy-headers \
  config.asgi:application
