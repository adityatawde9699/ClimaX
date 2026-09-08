# Data Layer Schemas & Specifications

This directory contains declarative schema specifications and validation contracts used across the ClimaX data ecosystem (FastAPI, BigQuery, PostgreSQL/PostGIS, and Frontend).

## Entity Schemas Catalog:
1. `user.schema.json` - System user and stakeholder roles.
2. `organization.schema.json` - Municipal bodies, environmental boards, and research institutions.
3. `sensor.schema.json` - IoT monitors, government stations, and satellite grid pixels.
4. `environmental_observation.schema.json` - Ground telemetry measurements (PM2.5, NO2, AQI).
5. `citizen_report.schema.json` - Citizen mobile submissions with multimedia references.
6. `ai_analysis.schema.json` - Multimodal AI inference results, confidence, and visual evidence.
7. `prediction.schema.json` - Spatio-temporal plume dispersion and forward forecasts.
8. `incident.schema.json` - Municipal incident lifecycle, assigned officers, and mitigation state.
9. `intervention.schema.json` - Targeted anti-pollution field operations.
10. `intervention_measurement.schema.json` - Pre/post intervention comparative delta metrics.
