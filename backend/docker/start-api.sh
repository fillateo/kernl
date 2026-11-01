#!/bin/sh
set -eu

cd /app

python manage.py migrate --noinput
python manage.py seed_catalog --prune

exec uvicorn config.asgi:application \
  --host 0.0.0.0 \
  --port 8000 \
  --workers "${WEB_CONCURRENCY:-2}" \
  --http httptools \
  --ws auto \
  --timeout-keep-alive 75 \
  --lifespan off \
  --no-server-header
