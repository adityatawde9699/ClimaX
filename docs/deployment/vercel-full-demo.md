# Vercel web + Vercel FastAPI demo

The web and API are separate Vercel projects in the same repository. The web
project uses `apps/web` as its Root Directory. The API project (`climax-api`)
uses the repository root, the **FastAPI** framework, and [app.py](../../app.py)
as its ASGI entrypoint. The API is one Vercel Function, not a persistent
Uvicorn server. Local ports 3000 and 8000 do not appear in production URLs.

## Database and credentials

Use an **isolated demo-only** Neon/PostGIS database or branch. Anyone visiting
the public login page can sign in as Citizen, Authority, or Researcher; the
Authority account can modify records. Never use the real-user database for this
public demo. Keep all database, JWT, Redis, and provider credentials in the API
project's encrypted Vercel environment variables, never in Git or
`NEXT_PUBLIC_*` variables. Rotate any secrets previously shared in chat.

Before the first deployment, configure these production variables on the
`climax-api` project:

| Variable | Value |
| --- | --- |
| `DATABASE_URL` | `postgresql+asyncpg://...` for the isolated demo database, with provider-required TLS options |
| `DATABASE_SYNC_URL` | `postgresql+psycopg2://...` for the **same** database |
| `JWT_SECRET_KEY` | New random secret of at least 32 characters |
| `REDIS_URL` | Hosted TLS Redis URL, if using cache (optional for basic demo) |
| `GEMINI_API_KEY` | Provider key, only if AI features are required (optional) |

The API project also needs `ENVIRONMENT=demo`, `ENABLE_DEMO_LOGIN=true`,
`DEBUG=false`, `ENABLE_API_DOCS=false`, `CORS_ORIGINS=["https://climaxevs.vercel.app"]`,
`DB_POOL_SIZE=2`, and `DB_MAX_OVERFLOW=1`. These are safe, non-secret settings.
Add other exact HTTPS frontend origins to `CORS_ORIGINS` for previews. Do not
use `*` with credentialed browser requests.

## Prepare the demo data once

Vercel Functions should not run migrations or seed data during each cold start.
Run migrations and the repeatable seed once from a trusted machine with the
**demo-only** database URLs set:

```bash
ENVIRONMENT=demo ENABLE_DEMO_LOGIN=true \
  alembic -c infrastructure/database/alembic.ini upgrade head
ENVIRONMENT=demo ENABLE_DEMO_LOGIN=true \
  PYTHONPATH=apps/api python scripts/seed-demo.py
```

The remaining required secure settings (especially `JWT_SECRET_KEY` and
`CORS_ORIGINS`) must also be present in the command environment or local
`apps/api/.env`. Check the target database before running either command.
`scripts/seed-demo.py` refuses production mode.

## Deploy and connect

Push the reviewed source to the repository and deploy the `climax-api` project
from that source. Set the API project's Root Directory to the repository root
and Framework Preset to FastAPI. Once the API has a public domain, check
`https://YOUR-API-DOMAIN/health`: it must return HTTP 200 with `database: healthy`.
No fixed `PORT` is needed for the Vercel Python runtime.

Set these production variables on the existing `climax` web project and
redeploy it, because `NEXT_PUBLIC_*` variables are baked in at build time:

| Variable | Value |
| --- | --- |
| `NEXT_PUBLIC_API_URL` | `https://YOUR-API-DOMAIN/api/v1` |
| `NEXT_PUBLIC_DEMO_MODE` | `true` |

The browser calls the API's HTTPS host directly. FastAPI allows the exact web
origin through CORS. For local development, `apps/web/.env` instead points to
`http://localhost:8000/api/v1`, while Next.js runs on `localhost:3000`.

Check all three login buttons on `/login`, then verify sensor markers, reports,
alerts, and forecasts. OSM tiles require no API key. This demo uses periodic
API queries instead of the app's in-memory WebSocket broker; multiple Vercel
function instances cannot share that broker. A production realtime channel
would need shared pub/sub or a dedicated realtime service.

Vercel's [FastAPI guide](https://vercel.com/docs/frameworks/backend/fastapi)
documents the Python entrypoint and single-function model; its
[monorepo guide](https://vercel.com/docs/monorepos) covers separate project
roots. Function bundle size and duration limits still apply to this API.
