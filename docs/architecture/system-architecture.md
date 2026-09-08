# ClimaX System Architecture Specification

## 1. Architectural Philosophy & Strategy

ClimaX is architected as an operational, high-throughput environmental command platform. Designed for reliability during severe public pollution crises and scalable hackathon execution, the platform adopts a **Modular Monolith** pattern. This maximizes developer velocity and cohesion while maintaining strict domain separation, completely avoiding the premature complexity, distributed transaction failure modes, and operational overhead of microservices.

```
                                    ┌──────────────────────┐
                                    │       CITIZENS       │
                                    │ (Mobile Web Browser) │
                                    └──────────┬───────────┘
                                               │
                                               │ HTTPS / WSS
                                               ▼
┌──────────────────────┐            ┌──────────────────────┐            ┌──────────────────────┐
│  MUNICIPAL COMMAND   │            │   NEXT.JS 14+ EDGE   │            │    RESEARCHERS &     │
│   (Desktop Console)  │◄───────────┤   (Cloud Run Web)    ├───────────►│    ADMINISTRATORS    │
└──────────────────────┘            └──────────┬───────────┘            └──────────────────────┘
                                               │
                                               │ REST / Streaming JSON
                                               ▼
                                    ┌──────────────────────┐
                                    │   FASTAPI BACKEND    │
                                    │   (Cloud Run API)    │
                                    └──────────┬───────────┘
                                               │
               ┌───────────────────────────────┼───────────────────────────────┐
               ▼                               ▼                               ▼
  ┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
  │   POSTGRESQL + POSTGIS  │     │   GOOGLE CLOUD PUBSUB   │     │    GOOGLE AI STUDIO     │
  │ • Spatial R-Tree Index  │     │ • Sensor Ingest Topic   │     │ • Gemini 1.5 Pro        │
  │ • Relational Entities   │     │ • Citizen Report Topic  │     │ • Gemini 1.5 Flash      │
  │ • Audit & Status Logs   │     │ • Alert Dispatch Topic  │     │ • Multimodal Reasoning  │
  └─────────────────────────┘     └────────────┬────────────┘     └─────────────────────────┘
                                               │
                                               ▼
                                  ┌─────────────────────────┐
                                  │   ANALYTICAL WAREHOUSE  │
                                  │ • Google BigQuery       │
                                  │ • Google Cloud Storage  │
                                  │ • Google Earth Engine   │
                                  │ • Vertex AI Endpoints   │
                                  └─────────────────────────┘
```

---

## 2. Core Closed-Loop Processing Topology

The architecture maps directly to the 6-stage product loop:

```
                  ┌─────────────────────────────────────────────────────────┐
                  │ 1. DETECT                                               │
                  │ • Ingest IoT sensor telemetry (MQTT/HTTP)               │
                  │ • Ingest Citizen photo/video reports via GCS            │
                  │ • Ingest Sentinel-5P / Landsat Earth Engine rasters     │
                  └────────────────────────────┬────────────────────────────┘
                                               ▼
                  ┌─────────────────────────────────────────────────────────┐
                  │ 2. UNDERSTAND                                           │
                  │ • Dispatch media to Gemini 1.5 Pro Multimodal           │
                  │ • Extract bounding box, smoke density, confidence       │
                  │ • Formulate explainable evidence payload                │
                  └────────────────────────────┬────────────────────────────┘
                                               ▼
                  ┌─────────────────────────────────────────────────────────┐
                  │ 3. PREDICT                                              │
                  │ • Feed meteorological wind vectors & current AQI        │
                  │ • Query Vertex AI spatio-temporal LSTM/Transformer     │
                  │ • Output 6h, 24h, 72h forward dispersion cone           │
                  └────────────────────────────┬────────────────────────────┘
                                               ▼
                  ┌─────────────────────────────────────────────────────────┐
                  │ 4. PRIORITIZE                                           │
                  │ • Execute PostGIS proximity query to sensitive receptors│
                  │ • Calculate multi-criteria Environmental Risk Score     │
                  │ • Triage high-risk events into Municipal Incidents      │
                  └────────────────────────────┬────────────────────────────┘
                                               ▼
                  ┌─────────────────────────────────────────────────────────┐
                  │ 5. ACT                                                  │
                  │ • Dispatch geofenced Citizen Push Alerts via FCM        │
                  │ • Assign municipal inspection field teams               │
                  │ • Route automated anti-smog gun / watering orders       │
                  └────────────────────────────┬────────────────────────────┘
                                               ▼
                  ┌─────────────────────────────────────────────────────────┐
                  │ 6. MEASURE                                              │
                  │ • Record post-intervention sensor readings at +1h to +6h│
                  │ • Compute statistically validated delta AQI             │
                  │ • Update municipal intervention effectiveness score     │
                  └────────────────────────────┬────────────────────────────┘
                                               │
                                               └───────► (Feeds back into Step 1)
```

---

## 3. Technology Selection Justification

| Technology | Selection Rationale |
| :--- | :--- |
| **Next.js 14+ (App Router)** | Fast server-side rendering, universal React component sharing, native streaming support for high-frequency map data, and effortless deployment to Cloud Run. |
| **FastAPI (Python 3.11+)** | High-performance asynchronous ASGI framework with native Pydantic v2 data validation, automated OpenAPI contract generation, and native integration with Google AI Python SDKs. |
| **PostgreSQL 16 + PostGIS** | Gold standard open-source spatial relational database. Provides R-Tree spatial indexing (`GIST`), polygon intersection queries, and spatial buffering. |
| **Google Cloud Run** | Fully managed serverless container runtime that scales from zero to hundreds of instances seamlessly during air quality crisis spikes without cluster management overhead. |
| **Google Gemini 1.5** | Industry-leading multimodal reasoning with immense context windows. Enables deep understanding of citizen images/videos alongside complex environmental meteorological context. |
| **Google Earth Engine** | Planetary-scale geospatial analysis platform providing immediate API access to Sentinel-5P NO2, Landsat, and MODIS atmospheric grids without hosting petabytes of rasters. |
| **Google BigQuery** | Serverless, highly scalable analytical data warehouse capable of querying billions of historical sensor observations in seconds at near-zero maintenance. |
