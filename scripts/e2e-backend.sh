#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON_BIN:-$ROOT_DIR/backend/.venv/bin/python}"
UVICORN="${UVICORN_BIN:-$ROOT_DIR/backend/.venv/bin/uvicorn}"

if [[ ! -x "$PYTHON" ]]; then
  echo "Backend virtualenv not found. Run 'make install' first." >&2
  exit 1
fi

cd "$ROOT_DIR/backend"
"$PYTHON" manage.py migrate --noinput
"$PYTHON" manage.py seed_catalog --prune

exec "$UVICORN" config.asgi:application --host 127.0.0.1 --port 8000
