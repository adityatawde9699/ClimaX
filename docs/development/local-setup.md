# Local development setup

## Prerequisites

Install Docker Compose v2, Python 3.11+, and Node.js 20+. Copy
`apps/api/.env.example` to `apps/api/.env` and `apps/web/.env.example` to
`apps/web/.env` before starting services. The setup script does this if the
files are absent.

## Start the platform

```bash
./scripts/setup-dev.sh
docker compose --env-file apps/web/.env \
  -f infrastructure/docker/docker-compose.yml up -d --build
```

The application starts with an empty database. Connect production ingestion sources or create
records through authenticated API workflows; local setup does not insert synthetic records.

Check the service health at `http://localhost:8000/health`, OpenAPI at `http://localhost:8000/docs`, and the web app at `http://localhost:3000`.

## Demo with sample data

In a development environment, run the migrations and seed the sample Delhi NCR dataset:

```bash
source .venv/bin/activate
alembic -c infrastructure/database/alembic.ini upgrade head
PYTHONPATH=apps/api python scripts/seed-demo.py
```

The seed is repeatable: it adds the three public demo roles and sample sensors,
observations, forecasts, hotspots, incidents, interventions, alerts, and a
citizen report. Running it again refreshes sample timestamps without creating
duplicate records. It refuses to run when `ENVIRONMENT=production`.

Set `ENABLE_DEMO_LOGIN=true` in `apps/api/.env` and
`NEXT_PUBLIC_DEMO_MODE=true` in `apps/web/.env`, then start the API and web app:

```bash
npm run dev:api
npm run dev:web
```

Open `http://localhost:3000/login` and choose Citizen, Authority, or Researcher.
The one-click endpoint is disabled by default and is unavailable in production.
The dashboard labels the sample dataset as demo data. External services such as
Vertex AI prediction generation and Google login still need their own provider
configuration; seeded forecast rows support the demo without those services.

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
