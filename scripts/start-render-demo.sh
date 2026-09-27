#!/bin/sh
set -eu

if [ "${ENVIRONMENT:-}" != "demo" ]; then
  echo "Refusing to seed or start the public demo outside ENVIRONMENT=demo" >&2
  exit 1
fi

cd /app
export PYTHONPATH=/app/apps/api
alembic -c infrastructure/database/alembic.ini upgrade head
python scripts/seed-demo.py
cd /app/apps/api
exec uvicorn main:app --host 0.0.0.0 --port "${PORT:-10000}" --no-access-log
