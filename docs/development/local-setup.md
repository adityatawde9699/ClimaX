# Local development setup

## Prerequisites

Install Docker Compose v2, Python 3.11+, and Node.js 20+. Copy `.env.example` to `.env` before starting services.

## Start the platform

```bash
./scripts/setup-dev.sh
cd infrastructure/docker
docker compose up -d --build
```

The application starts with an empty database. Connect production ingestion sources or create
records through authenticated API workflows; local setup does not insert synthetic records.

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
