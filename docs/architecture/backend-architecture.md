# Backend Architecture Specification

## 1. Clean Architecture & Layered Boundaries

The ClimaX backend is built with FastAPI (Python 3.11+) following strict Clean Architecture principles. Business logic is completely decoupled from HTTP transport, framework routers, and specific database engines.

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. API LAYER (`apps/api/api/v1/`)                                      │
│    • Pydantic request deserialization & response serialization         │
│    • HTTP Status codes, header validation, query parameters            │
│    • NO business logic or database queries                             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. DOMAIN SERVICE LAYER (`apps/api/services/`)                         │
│    • Core business rules and orchestration                             │
│    • Transaction boundaries & multi-repository coordination            │
│    • Invokes AI orchestration, prediction, and event bus               │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 3. REPOSITORY LAYER (`apps/api/repositories/`)                         │
│    • Encapsulates data access & query composition                      │
│    • Asynchronous SQLAlchemy 2.0 queries & PostGIS spatial filters     │
│    • In-memory mocking enabled for unit testing                        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 4. INFRASTRUCTURE & INTEGRATIONS (`apps/api/integrations/`)            │
│    • PostgreSQL / PostGIS database engine via AsyncPG                  │
│    • Google Cloud Storage, Cloud Pub/Sub, BigQuery                     │
│    • Gemini 1.5 API & Vertex AI Endpoints                              │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. API Versioning & Module Boundaries

All public endpoints are strictly versioned under `/api/v1/`:

| Module | Route Prefix | Primary Domain Responsibility |
| :--- | :--- | :--- |
| **Users** | `/api/v1/users` | Profile management, role assignments, auth session state. |
| **Reports** | `/api/v1/reports` | Citizen incident intake, media attachment verification, status tracking. |
| **Environment** | `/api/v1/environment` | Live atmospheric observations, spatial radius queries, weather feeds. |
| **Sensors** | `/api/v1/sensors` | Physical and low-cost sensor metadata, calibration state, health. |
| **Incidents** | `/api/v1/incidents` | Municipal operational incidents, officer assignment, lifecycle. |
| **Predictions** | `/api/v1/predictions` | 6h, 24h, 72h localized forecasting and Gaussian plume models. |
| **Risk** | `/api/v1/risk` | Composite Environmental Risk Index calculation and receptor exposure. |
| **Alerts** | `/api/v1/alerts` | Public advisory broadcast, threshold trigger notifications. |
| **Interventions** | `/api/v1/interventions` | Mitigation action logs (anti-smog guns) and impact delta tracking. |
| **Analytics** | `/api/v1/analytics` | High-level macro aggregations and historical trends. |
| **AI** | `/api/v1/ai` | Gemini multimodal analysis and AI Copilot conversational sessions. |

---

## 3. Asynchronous Database Access Pattern

- **Driver**: `asyncpg` combined with SQLAlchemy 2.0 declarative async session management.
- **Connection Pooling**: Static pool sizing configured via `core/config.py` (`DB_POOL_SIZE=20`, `DB_MAX_OVERFLOW=10`).
- **Spatial Queries**: PostGIS geometry types mapped natively via `geoalchemy2` and `shapely`, allowing direct spatial operations (e.g. `ST_DWithin`, `ST_Contains`) in ORM queries.
