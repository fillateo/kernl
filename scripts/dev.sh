#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$ROOT_DIR/backend/.venv/bin/python"
UVICORN="$ROOT_DIR/backend/.venv/bin/uvicorn"
BACKEND_PID=""

cleanup() {
  if [[ -n "$BACKEND_PID" ]] && kill -0 "$BACKEND_PID" 2>/dev/null; then
    kill "$BACKEND_PID" 2>/dev/null || true
    wait "$BACKEND_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

if [[ ! -x "$PYTHON" ]]; then
  echo "Backend virtualenv not found. Run 'make install' first." >&2
  exit 1
fi

if [[ ! -d "$ROOT_DIR/frontend/node_modules" ]]; then
  echo "Frontend dependencies not installed. Run 'make install' first." >&2
  exit 1
fi

cd "$ROOT_DIR/backend"
"$PYTHON" manage.py migrate --noinput
"$PYTHON" manage.py seed_catalog --prune

echo "Starting Django + Channels on http://127.0.0.1:8000"
"$UVICORN" config.asgi:application --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

cd "$ROOT_DIR/frontend"
export API_URL="${API_URL:-http://127.0.0.1:8000}"
export NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL:-http://127.0.0.1:8000}"

echo "Starting Next.js on http://localhost:3000"
npm run dev
