# Test Suite Scaffolding & Guidelines

ClimaX enforces a multi-level automated testing pyramid:

- `unit/`: Pure function, parser, and domain service unit tests with zero I/O dependencies.
- `api/`: FastAPI endpoint integration tests using `httpx.AsyncClient` against mock repositories.
- `geospatial/`: PostGIS spatial query validation, Haversine accuracy checks, and buffer calculations.
- `ai_eval/`: Synthetic benchmark tests measuring Gemini multimodal classification accuracy against labeled ground truth images.
- `integration/`: End-to-end multi-component tests verifying database persistence and Pub/Sub event dispatch.
- `e2e/`: Playwright / Cypress browser automation tests for Citizen reporting flows and Command Center dashboards.

All feature test implementations commence alongside their respective phases (Phases 1-13).
