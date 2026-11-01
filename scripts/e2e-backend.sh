#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON_BIN:-$ROOT_DIR/backend/.venv/bin/python}"
DAPHNE="${DAPHNE_BIN:-$ROOT_DIR/backend/.venv/bin/daphne}"

if [[ ! -x "$PYTHON" ]]; then
  echo "Backend virtualenv not found. Run 'make install' first." >&2
  exit 1
fi

cd "$ROOT_DIR/backend"
"$PYTHON" manage.py migrate --noinput
"$PYTHON" manage.py seed_catalog --prune

exec "$DAPHNE" -b 127.0.0.1 -p 8000 config.asgi:application
