# Local development setup

## Prerequisites

Install Docker Compose v2, Python 3.11+, and Node.js 20+. Copy `.env.example` to `.env` before starting services.

## Start the platform

```bash
./scripts/setup-dev.sh
cd infrastructure/docker
docker compose up -d --build
python ../../scripts/seed-db.py --env development
```

Check the service health at `http://localhost:8000/health`, OpenAPI at `http://localhost:8000/docs`, and the web app at `http://localhost:3000`.

## Database migrations

```bash
alembic -c infrastructure/database/alembic.ini upgrade head
alembic -c infrastructure/database/alembic.ini current
```

The initial revision is `0001` and creates the PostGIS extension and all canonical tables.

## Verification

```bash
python scripts/verify-scaffolding.py
pytest tests/architecture/
```
