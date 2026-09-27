# Public demo: Render API + Vercel web

This setup runs the FastAPI demo backend on Render and the Next.js frontend on
Vercel. The two services communicate over HTTPS: the browser calls
`https://YOUR-RENDER-HOST.onrender.com/api/v1`, and Render allows the exact
Vercel origin through `CORS_ORIGINS`. Port 8000 is only for local development.

## 1. Prepare an isolated demo database

Create a separate PostgreSQL/PostGIS database or Neon branch for the public
demo. The public login buttons issue Citizen, Authority, and Researcher tokens;
the Authority role can change demo data. **Do not connect this public demo to
the database used by real users.**

The API requires two connection strings for the same demo database:

- `DATABASE_URL`: `postgresql+asyncpg://...` for API requests.
- `DATABASE_SYNC_URL`: `postgresql+psycopg2://...` for Alembic migrations.

Keep the SSL options required by your database provider. Neither URL belongs
in Git, Vercel, or a `NEXT_PUBLIC_*` variable.

## 2. Deploy the API on Render

Create a Render Blueprint from the repository's [render.yaml](../../render.yaml).
It builds the API Docker image from the repository root, runs Alembic and the
repeatable demo seed at startup, then starts Uvicorn on Render's `PORT`. The
`/health` check requires a working database connection. The seed script refuses
to run in a production environment.

Enter these values in the Render environment/Blueprint prompt:

| Variable | Value |
| --- | --- |
| `DATABASE_URL` | Async connection to the isolated demo database |
| `DATABASE_SYNC_URL` | Sync connection to the same isolated demo database |
| `CORS_ORIGINS` | `["https://climaxevs.vercel.app"]`, replacing the hostname if your Vercel domain differs |
| `REDIS_URL` | Your hosted Redis TLS URL; use a separate demo cache when possible |

The Blueprint sets `ENVIRONMENT=demo`, `ENABLE_DEMO_LOGIN=true`, disables API
docs/debug, and generates a fresh JWT signing secret. It uses the free Render
plan; upgrade the plan if startup or cold-start performance is insufficient.
`GEMINI_API_KEY` can optionally be added as a Render secret. Google
login stays available when matching OAuth client IDs are configured, but is not
required for the demo. Never put the earlier API credentials into Git.

Open `https://YOUR-RENDER-HOST.onrender.com/health` and confirm it reports a
healthy database before deploying the web app. If you created an existing
Render service instead of a Blueprint, use the same Dockerfile and set the
Docker command to `sh /app/scripts/start-render-demo.sh`.

## 3. Deploy the web app on Vercel

Import the same Git repository as a Next.js project. Set its **Root Directory**
to `apps/web`. Keep workspace files from outside that directory available to
the build; `apps/web` depends on `packages/*` in the repository. The framework
should be Next.js, with the default npm workspace installation. No API
credentials or database URLs go in the Vercel project.

Set these Vercel project variables for the deployment environment:

| Variable | Value |
| --- | --- |
| `NEXT_PUBLIC_API_URL` | `https://YOUR-RENDER-HOST.onrender.com/api/v1` |
| `NEXT_PUBLIC_DEMO_MODE` | `true` |
| `NEXT_PUBLIC_OSM_TILE_URL` | `https://tile.openstreetmap.org/{z}/{x}/{y}.png` (optional; already the default) |

`NEXT_PUBLIC_API_URL` must use HTTPS and end in `/api/v1`; the Vercel build
fails instead of silently shipping a `localhost:8000` API URL. Public frontend
variables are embedded at build time, so redeploy the web app after changing
them. Keep Google Maps variables only if you later add Google keys; OSM works
without a key.

For Vercel preview domains, add each exact HTTPS preview origin to Render's
`CORS_ORIGINS` JSON array, then redeploy the API. Do not use a wildcard origin
with credentialed browser requests.

## 4. Verify the deployed demo

1. Confirm Render `/health` returns 200 with `database: healthy`.
2. Open the Vercel `/login` page and click Citizen, Authority, and Researcher
   in separate sessions. They should land on Reports, Dashboard, and Map.
3. Check that the map displays OSM tiles and six demo sensors, and that Reports,
   Hotspots, Alerts, and Forecast contain sample data.
4. In browser DevTools, API requests should target the Render HTTPS host, never
   `localhost:8000`; no CORS errors should appear.

The dataset is synthetic and is refreshed whenever the Render instance starts.
Provider-backed features such as Google login, media uploads, and live Vertex
forecast generation still require their respective provider configuration.

References: [Render Blueprints](https://render.com/docs/blueprint-spec),
[Render health checks](https://render.com/docs/health-checks),
[Vercel monorepos](https://vercel.com/docs/monorepos), and
[Vercel environment variables](https://vercel.com/docs/environment-variables).
