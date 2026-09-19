# ClimaX

ClimaX is an environmental intelligence and response platform. It combines sensor observations, citizen reports, forecasts, risk assessments, and municipal interventions in one operational dashboard.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776ab.svg)](pyproject.toml)
[![Next.js](https://img.shields.io/badge/Next.js-16-black.svg)](apps/web)

> The application starts with an empty database. Production data is added through authenticated APIs and configured ingestion providers; no demo records are required at runtime.

## What it does

- Displays live environmental observations, AQI guidance, sensors, risk hotspots, predictions, incidents, alerts, and interventions.
- Accepts citizen pollution reports with optional JPEG, PNG, WebP, or MP4 evidence uploaded through signed Google Cloud Storage URLs.
- Creates incidents automatically for configured `VERY_HIGH` and `CRITICAL` risk assessments.
- Dispatches and tracks interventions through an incident lifecycle:

  `OPEN → INVESTIGATING → DISPATCHED → MITIGATED → RESOLVED`

- Streams operational events over an authenticated WebSocket and shows high-severity alert toasts in the web app.
- Uses Redis as a best-effort cache for prediction responses and risk hotspots.

## Architecture

```text
Next.js web app ── REST / WebSocket ── FastAPI API
                                          │
                             ┌────────────┼────────────┐
                             │            │            │
                         PostGIS       Redis       GCP adapters
                      data + spatial   cache     GCS · Pub/Sub
                                                   Gemini · Vertex
```

The repository is a modular monolith: API routers handle transport, services hold domain rules, repositories handle persistence, and integrations isolate cloud providers.

## Repository layout

```text
apps/api/                 FastAPI application, models, services, and adapters
apps/web/                 Next.js dashboard and citizen reporting UI
packages/                 Shared TypeScript packages
services/                 Provider and domain service boundaries
infrastructure/database/  SQL schema and Alembic migrations
infrastructure/docker/    Local PostGIS, Redis, API, and web containers
infrastructure/gcp/       Cloud Run, Pub/Sub, and GCP deployment manifests
docs/                     Architecture, product, API, and deployment guides
scripts/                  Validation, load-test, and operational utilities
tests/                    Unit, integration, and browser tests
```

## Quick start

### Prerequisites

- Node.js 20+
- Python 3.11+
- Docker and Docker Compose

### 1. Install dependencies

```bash
cp .env.example .env
npm install
python3 -m pip install -e ".[dev]"
```

If pip reports `resolution-too-deep`, install the project with a current Python 3.11–3.13 environment and upgrade pip first:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### 2. Start local infrastructure

```bash
docker compose -f infrastructure/docker/docker-compose.yml up -d postgres redis
alembic -c infrastructure/database/alembic.ini upgrade head
```

The local database is PostgreSQL 16 with PostGIS. The compose file exposes PostgreSQL on `5432` and Redis on `6379`.

### 3. Start the API and web app

Use two terminals:

```bash
npm run dev:api      # http://127.0.0.1:8000
npm run dev:web      # http://127.0.0.1:3000
```

The API documentation is available at `http://127.0.0.1:8000/docs` when `ENABLE_API_DOCS=true`.

### 4. Create an account

Open `http://127.0.0.1:3000/register` and create a local account. Manual email/password login is available at `/login`. Google login requires the OAuth variables in `.env` and a matching callback configuration in Google Cloud.

## Useful commands

```bash
# Backend checks
ruff check apps/api services scripts tests infrastructure/database/alembic
PYTHONPATH=apps/api pytest -q

# Frontend checks
npm run lint:web
npm run typecheck:web
npm run build:web

# Mobile browser validation at 375px
npx playwright install chromium
npm run test:e2e

# Dependency security check
npm audit --omit=dev
```

For a running web server on another port, reuse it during browser tests:

```bash
PLAYWRIGHT_BASE_URL=http://127.0.0.1:3000 npm run test:e2e
```

## Configuration

`.env.example` documents all supported settings. The most important local values are:

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | Async SQLAlchemy connection string |
| `DATABASE_SYNC_URL` | Alembic and synchronous tooling connection string |
| `REDIS_URL` | Optional response cache; cache failures fail open |
| `JWT_SECRET_KEY` | Local JWT signing key; use a secret of at least 32 bytes |
| `CORS_ORIGINS` | JSON array of allowed web origins |
| `GCS_BUCKET` | Bucket for citizen report evidence |
| `GOOGLE_OAUTH_CLIENT_ID` | API OAuth client identifier |
| `NEXT_PUBLIC_API_URL` | Browser-facing API base URL |
| `RISK_AUTO_INCIDENT_ORGANIZATION_ID` | Authority organization for automatic risk incidents |

Provider-backed features such as Gemini, Vertex AI, Earth Engine, Pub/Sub, and GCS return explicit configuration errors when credentials are absent; they do not silently generate synthetic production data.

## Production validation

The deployment checklist is in [docs/deployment/production-checklist.md](docs/deployment/production-checklist.md). After deploying the API, run the non-mutating HTTP and WebSocket smoke probe with an authenticated token:

```bash
CLIMAX_PRODUCTION_URL=https://api.example.com \
CLIMAX_SMOKE_TOKEN='<jwt>' \
python scripts/validate-production.py
```

Cloud-only tasks still require access to the target project: applying Cloud Run and Pub/Sub manifests, configuring Secret Manager and Cloud SQL, granting service-account IAM roles, enabling SMS/push providers, and configuring Cloud Monitoring alerts.

## Documentation

- [Local development](docs/development/local-setup.md)
- [API guide](docs/api/README.md)
- [System architecture](docs/architecture/system-architecture.md)
- [Backend architecture](docs/architecture/backend-architecture.md)
- [Frontend architecture](docs/architecture/frontend-architecture.md)
- [Security and privacy](docs/architecture/security.md)
- [Production checklist](docs/deployment/production-checklist.md)
- [Roadmap and implementation status](ROADMAP.md)
- [Contributing](CONTRIBUTING.md)

## License

ClimaX is licensed under the Apache License 2.0. See [LICENSE](LICENSE).
