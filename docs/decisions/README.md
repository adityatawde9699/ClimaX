# Architecture Decision Records (ADRs)

This directory records the significant architectural decisions made for the ClimaX platform.

---

## ADR-001: Adoption of Modular Monolith over Microservices

### Status
Accepted

### Context
Building a multi-stakeholder environmental platform under hackathon and rapid-evolution conditions requires rapid iteration, atomic database transactions across incidents and verifications, and low operational friction. Microservices introduce premature networking latency, distributed transaction complexity, and excessive deployment overhead.

### Decision
Implement ClimaX as a **Modular Monolith**. Code is partitioned into strict domain modules (`apps/api/api/v1/`, `services/*`, `packages/*`), allowing independent domain isolation while maintaining single-process deployments on Google Cloud Run.

### Consequences
- **Positive**: Simplified CI/CD, atomic database transactions, shared in-memory models, faster development velocity.
- **Negative**: Requires strict developer discipline to avoid circular cross-module imports (enforced via architecture tests).

---

## ADR-002: Technology Stack: Next.js 14+ and FastAPI

### Status
Accepted

### Context
The platform requires a fast, responsive, mobile-optimized UI for citizens and high-density dashboards for authorities, paired with a backend optimized for Python-native AI/ML ecosystems (Gemini SDK, Vertex AI, Earth Engine, Shapely, GeoPandas).

### Decision
- **Frontend**: Next.js 14+ with TypeScript and Tailwind CSS.
- **Backend**: Python 3.11+ with FastAPI, AsyncPG, and SQLAlchemy 2.0.

### Consequences
- **Positive**: Native access to Google AI Python libraries, automatic OpenAPI documentation, asynchronous event concurrency, excellent server-side rendering for maps and metadata.
- **Negative**: Multi-language monorepo requires coordination between Node.js and Python toolchains (managed via root package.json and pyproject.toml).

---

## ADR-003: Separation of Spatial Transnational Store (PostGIS) and Analytical Warehouse (BigQuery)

### Status
Accepted

### Context
Continuous environmental IoT telemetry generates millions of readings daily. Executing complex real-time spatial joins on active incidents inside an analytical warehouse introduces prohibitive query latency and cost, while storing years of high-frequency sensor readings in PostgreSQL degrades OLTP performance.

### Decision
- **PostgreSQL 16 + PostGIS**: Primary OLTP database for active entities, incident queues, and real-time spatial buffer queries.
- **Google BigQuery**: Long-term analytical warehouse for historical telemetry, satellite grid timeseries, and researcher exports.

### Consequences
- **Positive**: Sub-second operational spatial queries in Command Center; cost-effective serverless querying of petabyte-scale historical archives.
- **Negative**: Requires an asynchronous synchronization pipeline (Cloud Pub/Sub) between Postgres and BigQuery.

---

## ADR-004: 4-Tier Environmental Information Trust Taxonomy

### Status
Accepted

### Context
Using AI in government environmental enforcement carries high liability. Hallucinations or misunderstood forward predictions can trigger unwarranted legal action against industrial operators or cause unnecessary public panic.

### Decision
Mandate that all data across storage, APIs, and UI explicitly carry one of four immutable tier tags: `OBSERVED`, `INFERRED`, `PREDICTED`, `VERIFIED`.

### Consequences
- **Positive**: Uncompromising trust and transparency for municipal officers and the public; zero ambiguity between measurement and hypothesis.
- **Negative**: All API schemas and data pipelines must propagate the tier metadata field.
