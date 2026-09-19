# Production deployment checklist

ClimaX deliberately refuses to start in `production` when development security defaults remain.

## Required configuration

Set these values through the deployment platform or Secret Manager:

- `ENVIRONMENT=production`
- `DEBUG=false`
- `ENABLE_API_DOCS=false`
- `JWT_SECRET_KEY` to a randomly generated value of at least 32 bytes
- `DATABASE_URL` and `DATABASE_SYNC_URL` with production credentials
- `CORS_ORIGINS` to a JSON array containing only deployed HTTPS web origins
- `NEXT_PUBLIC_API_URL` to the public API `/api/v1` URL
- `GOOGLE_OAUTH_CLIENT_ID` and `NEXT_PUBLIC_GOOGLE_CLIENT_ID` to the same web client ID
- `AUTHORITY_REGISTRATION_CODE` through Secret Manager, or leave it empty to disable Authority enrollment
- Google Cloud, Gemini, Vertex AI, Pub/Sub, Redis, and storage variables used by the enabled services
- `RISK_AUTO_INCIDENT_ORGANIZATION_ID` to the authority organization that owns automatically created incidents
- `PREDICTION_CACHE_TTL_SECONDS=3600` and `RISK_CACHE_TTL_SECONDS=900`
- `MAX_REPORT_UPLOAD_BYTES` and `GCS_BUCKET`; configure bucket CORS to allow the deployed web origin to `PUT` the accepted media types

## Release verification

```bash
alembic -c infrastructure/database/alembic.ini upgrade head
ruff check apps/api services tests scripts
PYTHONPATH=apps/api pytest -q
npm run lint:web
npm run typecheck:web
npm run build:web
npm run test:e2e
npm audit --omit=dev
```

After deployment, verify `/health` returns HTTP 200. A failed database check returns HTTP 503 so the
deployment platform will not route traffic to an unhealthy instance. Prediction requests also return
HTTP 503 until a real Vertex AI endpoint is configured; no synthetic forecast is substituted.

Run the non-mutating deployed HTTP and WebSocket probe with an authenticated token:

```bash
CLIMAX_PRODUCTION_URL=https://api.example.com \
CLIMAX_SMOKE_TOKEN='<jwt>' \
python scripts/validate-production.py
```

The probe checks health and primary read endpoints, opens an authenticated WebSocket, emits a
non-persistent realtime probe event, and verifies that the same event arrives within ten seconds.
