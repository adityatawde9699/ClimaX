# ClimaX — Federated AI Environmental Intelligence & Action Platform

[![Implementation Phase](https://img.shields.io/badge/Phases-0--2%20Implemented-success.svg)](#development-phases)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-green.svg)](pyproject.toml)
[![Next.js](https://img.shields.io/badge/Next.js-14%2B-black.svg)](apps/web)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-Vertex_AI_%7C_Earth_Engine-4285F4.svg)](docs/architecture/system-architecture.md)

> **Phases 1–2 Status Notice**: Local development foundations and the core database-backed API are implemented, including PostGIS migrations, deterministic seed data, JWT/RBAC security, CRUD routes, geospatial queries, and automated validation. Phase 3 is the next delivery milestone.

---

## 1. Executive Summary & Problem Space

Air and environmental pollution represents one of the most pressing planetary emergencies of our century, causing over 7 million premature deaths annually and crippling urban economic productivity. Current municipal environmental monitoring systems suffer from three fatal structural limitations:

1. **Severe Sensor Sparsity**: Physical reference-grade monitoring stations (e.g. BAM-1020) cost upwards of $30,000 each, resulting in vast urban and rural "blind zones" where hyper-local pollution spikes go completely undetected.
2. **Disconnected Citizen Feedback**: Citizen complaints sent via social media or legacy municipal helplines lack structured geolocation, standardized pollutant categorization, and verifiable atmospheric context, creating noise rather than actionable intelligence.
3. **Lagging Reactive Interventions**: Environmental departments operate reactively rather than predictively—dispatching sprinkler trucks, industrial inspectors, or traffic restrictions hours after hazardous plumes have already dispersed through population centers.

**ClimaX** bridges this chasm by establishing a **Federated AI Environmental Intelligence and Action Platform**. It unifies ground-level citizen reports, multimodal visual imagery, IoT sensor meshes, government reference monitors, meteorological forecasts, and Earth observation satellite feeds into a continuous, closed-loop environmental command system.

---

## 2. The Core Product Loop

ClimaX operates on a cyclical, 6-stage closed-loop operational pipeline:

```
  ┌────────────────────────────────────────────────────────┐
  │                        DETECT                          │
  │  (Citizen Photos/Video, IoT Sensors, Satellite Feeds)  │
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │                      UNDERSTAND                        │
  │  (Gemini Multimodal Analysis, Source Attribution,      │
  │               Explainable Evidence)                    │
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │                       PREDICT                          │
  │  (Vertex AI Spatio-temporal Plume Models, 6h-72h AQI)  │
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │                      PRIORITIZE                        │
  │  (Environmental Risk Engine, Population Vulnerability) │
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │                         ACT                            │
  │  (Incident Dispatch, Citizen Alerts, Task Assignment)  │
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │                       MEASURE                          │
  │  (Pre/Post Intervention Delta, Causal Impact Metrics)  │
  └───────────────────────────┬────────────────────────────┘
                              │
                              └───────► (Feeds back into DETECT)
```

1. **Detect**: Ingest continuous multi-source data across citizen mobile submissions, low-cost sensor networks, government APIs, and satellite imagery (Sentinel-5P / Landsat).
2. **Understand**: Use Gemini 1.5 multimodal models to classify pollution sources (e.g. open biomass burning, diesel generator exhaust, road dust), extract visual evidence, and assess confidence.
3. **Predict**: Forecast pollutant transport, dispersion, and AQI spikes across 6h, 24h, and 72h windows using atmospheric physics fused with Vertex AI sequence models.
4. **Prioritize**: Calculate an objective composite Risk Index factoring in pollutant severity, wind trajectory, and demographic exposure (schools, hospitals, dense residential zones).
5. **Act**: Convert high-priority risks into actionable municipal incidents, dispatching field enforcement units, anti-smog guns, or issuing localized citizen health advisories.
6. **Measure**: Continuously track sensor readings and follow-up citizen verification post-intervention to quantify atmospheric improvement and validate municipal efficacy.

---

## 3. Persona Journeys & Value Matrix

ClimaX is purpose-engineered to serve four key stakeholder personas:

| Stakeholder | Key Interfaces | Core Capabilities |
| :--- | :--- | :--- |
| **Citizens** | Mobile-responsive Web App (`/citizen`) | Real-time hyper-local air quality map, 1-tap photo/video incident reporting, AI-assisted symptom/exposure advisories, track municipal resolution progress. |
| **Government / Municipal Authorities** | Environmental Command Center (`/command-center`) | Real-time spatial incident queue, AI-suggested field team assignments, before/after intervention impact measurement, automated compliance audits. |
| **Environmental Researchers** | Data Explorer & Workspace (`/data-explorer`) | Direct access to historical BigQuery datasets, Earth Engine satellite rasters, spatial correlation tools, open data export (GeoJSON, NetCDF, CSV). |
| **System Administrators** | Admin Portal (`/admin`) | Sensor telemetry monitoring, AI model drift tracking, role-based access control (RBAC), ingestion pipeline health, threshold configuration. |

---

## 4. Core AI Concept: The 4-Tier Trust & Explainability Taxonomy

In high-stakes environmental governance, ungrounded AI hallucination can trigger false municipal panic or unwarranted legal penalties against industrial facilities. ClimaX solves this through an architectural separation of information types:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. OBSERVED DATA                                                            │
│    Physical, un-manipulated telemetry or direct citizen inputs.             │
│    Examples: IoT Sensor PM2.5 = 186 µg/m³, Citizen uploaded photo.          │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. AI INFERENCE                                                             │
│    Probabilistic interpretations produced by vision or language models.     │
│    Examples: "Possible tyre burning — 84% confidence (smoke plume detected)".│
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. PREDICTION                                                               │
│    Forward-looking estimates produced by spatio-temporal predictive models. │
│    Examples: "Predicted AQI at Ward 14 in 6 hours: 215 (Unhealthy)".        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. HUMAN VERIFICATION                                                       │
│    Definitive ground truth recorded by certified municipal field officers.  │
│    Examples: "Confirmed industrial boiler failure; ceased operations at 14:00"│
└─────────────────────────────────────────────────────────────────────────────┘
```

Every AI inference and prediction payload in ClimaX follows a standardized contract:
```json
{
  "result": "Biomass burning detected",
  "confidence": 0.88,
  "evidence": ["Black smoke plume with localized ground ash texture in bounding box [120, 45, 340, 510]"],
  "data_sources": ["citizen_upload:img_98124.jpg", "sensor:aq_del_12"],
  "model": "gemini-1.5-pro-vision-climax-v1",
  "timestamp": "2026-09-08T16:30:00Z",
  "verification_status": "unverified"
}
```

---

## 5. Technology Architecture Stack

### Monolithic Clean Architecture (Modular Monolith)
ClimaX avoids premature microservice overhead during MVP and hackathon execution, employing a strictly bounded **modular monolith** with clear package interfaces.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ FRONTEND: Next.js 14+ App Router, React 18, TypeScript, Tailwind CSS      │
│ (Feature-based: Command Center, Pollution Map, Citizen Portal, Data Studio)│
└─────────────────────────────────────┬──────────────────────────────────────┘
                                      │ REST API / WebSocket
                                      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ BACKEND: Python 3.11+ / FastAPI Modular Monolith                           │
│ (Clean Architecture: API Routes → Domain Services → Repositories → DB)     │
└───────────────────────┬───────────────────────────────┬────────────────────┘
                        │                               │
                        ▼                               ▼
┌───────────────────────────────────┐   ┌────────────────────────────────────┐
│ DATABASE & SPATIAL ENGINE         │   │ GOOGLE CLOUD & AI FOUNDATION       │
│ • PostgreSQL 16 + PostGIS         │   │ • Gemini 1.5 Pro & Flash (Vision)  │
│ • Spatial R-Tree Indexing         │   │ • Vertex AI Custom Endpoints       │
│ • Temporal TimescaleDB Partitions │   │ • Google Earth Engine API          │
│ • AsyncPG + SQLAlchemy 2.0        │   │ • BigQuery Environmental Warehouse │
│                                   │   │ • Google Maps Platform             │
│                                   │   │ • Cloud Storage & Cloud Pub/Sub    │
└───────────────────────────────────┘   └────────────────────────────────────┘
```

---

## 6. Repository Directory Structure

```text
climax/
├── apps/
│   ├── web/                    # Next.js 14+ Frontend application (Citizen & Authority UI)
│   │   ├── app/                # App router route groups: (citizen), (authority), (admin)
│   │   ├── components/         # Shared UI, layout, map controls, feedback components
│   │   ├── features/           # Feature boundaries (command-center, incidents, predictions...)
│   │   ├── hooks/              # Custom React hooks (useGeolocation, usePollutionData)
│   │   ├── lib/                # Client utility libraries & API client
│   │   ├── styles/             # Tailwind & design system token definitions
│   │   └── types/              # Frontend-specific type augmentations
│   └── api/                    # FastAPI Backend application
│       ├── api/v1/             # Versioned REST router endpoints
│       ├── core/               # App configuration, logging, exceptions, middleware
│       ├── models/             # SQLAlchemy / SQLModel ORM entity declarations
│       ├── schemas/            # Pydantic v2 DTO request & response contracts
│       ├── repositories/       # Data access interfaces & query builders
│       ├── services/           # Domain business logic contracts
│       ├── integrations/       # External adapters (GCP, Gemini, Maps, Weather)
│       ├── ai/                 # Gemini multimodal, reasoning, and copilot contracts
│       ├── prediction/         # Vertex AI prediction client contracts
│       ├── geospatial/         # PostGIS queries, GeoJSON parsers, spatial buffers
│       ├── events/             # Cloud Pub/Sub event publishers & subscribers
│       ├── workers/            # Background tasks & batch ingestion
│       ├── security/           # JWT, RBAC guards, PII redaction, sanitization
│       └── observability/      # OpenTelemetry, Prometheus metrics, structured logs
├── packages/                   # Reusable shared monorepo packages
│   ├── ui/                     # Government-grade headless design tokens & components
│   ├── types/                  # Canonical TypeScript entity interfaces & AI contracts
│   ├── config/                 # Shared Tailwind, ESLint, Prettier, TS configurations
│   └── utils/                  # Shared geospatial math, date formatters, sanitizers
├── services/                   # Independent service boundaries
│   ├── ai/                     # Multimodal prompts, vision pipelines, reasoning
│   ├── prediction/             # Spatio-temporal dispersion & ML models
│   ├── geospatial/             # GeoTIFF processing, Earth Engine raster pipelines
│   ├── environmental-data/     # IoT ingestion, CPCB/EPA government connectors
│   ├── alerts/                 # Multi-channel notification routing & SMS/Push
│   └── analytics/              # BigQuery aggregation & reporting pipelines
├── data/                       # Schemas, seed data, and fixtures
│   ├── schemas/                # Canonical JSON Schema specifications for 16 entities
│   ├── samples/                # Sample raw sensor feeds, citizen reports, AI inferences
│   └── fixtures/               # Seed data for baseline local testing
├── infrastructure/             # Deployment & cloud configuration
│   ├── docker/                 # Container definitions & local docker-compose
│   ├── gcp/                    # Cloud Run configs, BigQuery DDL, Pub/Sub manifests
│   ├── database/               # PostgreSQL + PostGIS migrations & SQL schema
│   └── deployment/             # CI/CD workflow manifests
├── docs/                       # Comprehensive technical & product documentation
│   ├── architecture/           # System, frontend, backend, AI, data, geospatial, security
│   ├── product/                # Product mission, user roles, persona journeys
│   ├── ai/                     # Trust, explainability, 4-tier taxonomy, confidence scoring
│   ├── data/                   # Data sources catalog, ingestion specs, licensing
│   └── decisions/              # Architecture Decision Records (ADRs)
├── scripts/                    # Development & verification utility scripts
├── tests/                      # Architecture, integration, and E2E test suites
├── .env.example                # Exhaustive environment variable template
├── .gitignore                  # Standardized VCS ignore rules
├── package.json                # Monorepo root workspace manifest
├── pyproject.toml              # Root Python tooling & dependency specification
├── ruff.toml                   # Python linting & formatting standards
├── CONTRIBUTING.md             # Contribution & development standards
└── LICENSE                     # Apache 2.0 Open Source License
```

---

## 7. Development Roadmap

ClimaX follows a disciplined 14-phase implementation plan:

- **Phase 0: Architecture & Scaffolding (Current Phase)**
  - Repository structure, configuration scaffolding, type definitions, schemas, and architecture documentation. Zero feature logic.
- **Phase 1: Frontend Foundation & Design System**
  - Implement the government-grade design token system, Tailwind palette, base layouts, navigation, and role-based shell.
- **Phase 2: Backend Foundation & Database**
  - PostgreSQL + PostGIS setup, Alembic migrations for 16 core entities, repository patterns, and base API v1 scaffolding.
- **Phase 3: Environmental Data Ingestion**
  - Connectors for OpenAQ, CPCB, weather APIs, and IoT sensor ingestion pipelines with deduplication.
- **Phase 4: Citizen Reporting**
  - Mobile reporting interface, photo upload to Google Cloud Storage, GPS reverse-geocoding, and report tracking.
- **Phase 5: Gemini Multimodal Analysis**
  - Integration with Gemini 1.5 Flash/Pro for image/video pollution classification, evidence extraction, and severity scoring.
- **Phase 6: Pollution Prediction**
  - Vertex AI predictive models forecasting 6h, 24h, and 72h localized pollutant concentrations and plume trajectory.
- **Phase 7: Pollution Source Intelligence**
  - Spatial correlation linking sensor spikes, wind vectors, and industrial zones to pinpoint likely emission culprits.
- **Phase 8: Environmental Risk Engine**
  - Composite multi-criteria risk scoring engine factoring in AQI, pollutant duration, and demographic vulnerability.
- **Phase 9: Alerts & Incident Management**
  - Authority incident command workflow, field team assignment, citizen push alerts, and status lifecycle.
- **Phase 10: AI Copilot**
  - Natural language environmental assistant for authorities and citizens powered by grounded Gemini reasoning.
- **Phase 11: Intervention Tracking**
  - Intervention logging (anti-smog guns, road watering, industrial notices) and pre/post atmospheric impact delta analysis.
- **Phase 12: Federated Learning Demonstration**
  - Edge model concept demonstrating privacy-preserving on-device smoke detection model updates across citizen nodes.
- **Phase 13: Production Hardening & Cloud Deployment**
  - Cloud Run deployment, BigQuery export pipelines, security audits, rate-limiting, and end-to-end stress testing.

---

## 8. Local Setup Prerequisites (Future Development)

When transitioning to Phase 1 and beyond:

1. **System Dependencies**:
   - Node.js 20.x or later
   - Python 3.11 or later
   - Docker & Docker Compose
2. **Environment File**:
   ```bash
   cp .env.example .env
   # Populate GCP_PROJECT_ID, GEMINI_API_KEY, and DB credentials for local testing
   ```
3. **Verify Scaffolding**:
   ```bash
   python3 scripts/verify-scaffolding.py
   ```

---

## 9. Architectural Documentation Index

| Topic | Document Path |
| :--- | :--- |
| **System Architecture** | [system-architecture.md](docs/architecture/system-architecture.md) |
| **Frontend Architecture** | [frontend-architecture.md](docs/architecture/frontend-architecture.md) |
| **Backend Architecture** | [backend-architecture.md](docs/architecture/backend-architecture.md) |
| **AI Architecture** | [ai-architecture.md](docs/architecture/ai-architecture.md) |
| **Data Architecture** | [data-architecture.md](docs/architecture/data-architecture.md) |
| **Geospatial Architecture** | [geospatial-architecture.md](docs/architecture/geospatial-architecture.md) |
| **Security & Privacy** | [security.md](docs/architecture/security.md) |
| **Observability & Metrics** | [observability.md](docs/architecture/observability.md) |
| **Product Overview** | [product-overview.md](docs/product/product-overview.md) |
| **User Roles & Personas** | [user-roles.md](docs/product/user-roles.md) |
| **Trust & Explainability** | [trust-and-explainability.md](docs/ai/trust-and-explainability.md) |
| **Data Sources Catalog** | [data-sources.md](docs/data/data-sources.md) |
| **Architecture Decision Records** | [decisions/README.md](docs/decisions/README.md) |
