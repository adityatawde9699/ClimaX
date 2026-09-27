# Deploy the frontend and API separately

The Next.js frontend (`apps/web`) and FastAPI backend (`apps/api`) are separate
services. They share this repository, but neither container needs the other
container to start. Build each image from the repository root because the web
app uses `packages/*` and the API uses `services/*`.

## API

Provision PostgreSQL with PostGIS and set `DATABASE_URL` and
`DATABASE_SYNC_URL` to that database. Set the API variables from
`apps/api/.env.example`, especially `JWT_SECRET_KEY`, `CORS_ORIGINS`,
`ENVIRONMENT=production`, `DEBUG=false`, and `ENABLE_API_DOCS=false`.
`CORS_ORIGINS` must be a JSON array containing the frontend's HTTPS origin.

The API image includes the Alembic migrations. Copy the API template to
`apps/api/.env` and configure it, then run the migration and start the API:

```bash
docker compose -f infrastructure/docker/compose.api.yml build
docker compose -f infrastructure/docker/compose.api.yml run --rm -w /app api \
  alembic -c infrastructure/database/alembic.ini upgrade head
docker compose -f infrastructure/docker/compose.api.yml up -d
```

The API serves port 8000 by default. Check `http://localhost:8000/health`.
For a cloud deployment, use the API image and
`infrastructure/gcp/cloud-run-api.yaml` with your project's values and secrets.

## Frontend

Copy `apps/web/.env.example` to `apps/web/.env`. Set `NEXT_PUBLIC_API_URL` to
the browser-accessible API URL ending in `/api/v1`. Set
`NEXT_PUBLIC_GOOGLE_CLIENT_ID` before building if Google login
is enabled. Next.js embeds these public values in the browser bundle, so
rebuild the image when the URL or client ID changes.

```bash
docker compose --env-file apps/web/.env \
  -f infrastructure/docker/compose.web.yml build
docker compose -f infrastructure/docker/compose.web.yml up -d
```

The frontend serves port 3000 by default. For a cloud deployment, use the web
image and `infrastructure/gcp/cloud-run-web.yaml` with your project's values.

The two Compose files have no service dependency on one another. The backend
still needs a reachable PostgreSQL/PostGIS database. Redis and provider
credentials are needed for the features that use them. The original
`docker-compose.yml` remains a local all-in-one development setup with
development database credentials.
