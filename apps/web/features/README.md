# Frontend Feature Architecture

ClimaX follows a strictly bounded, feature-first frontend structure. Each feature encapsulates its own:
- `components/`: Internal UI widgets specific to the feature.
- `hooks/`: Specialized state hooks.
- `services/`: API integration calls.
- `types/`: Feature-local view models.

## Feature Modules:
1. `command-center/`: Real-time operational situational awareness dashboard for municipal leadership.
2. `pollution-map/`: High-performance WebGL/Mapbox/Google Maps vector tile rendering engine.
3. `incidents/`: Incident lifecycle triage, dispatch, and resolution workflows.
4. `citizen-reports/`: Citizen reporting stream, photo viewer, and geolocation verification.
5. `predictions/`: Spatio-temporal plume dispersion visualizations and forecast timelines.
6. `source-intelligence/`: Back-trajectory wind analysis and emitter attribution.
7. `alerts/`: Broadcast alert builder and threshold notification center.
8. `interventions/`: Anti-smog measures, field unit tracking, and pre/post delta metrics.
9. `analytics/`: Historical trend analysis, compliance charts, and ward-by-ward scorecards.
10. `ai-copilot/`: Interactive environmental assistant with grounded citations.
11. `data-explorer/`: Geospatial dataset query builder and export studio.
12. `settings/`: Organization boundary configuration and alert thresholds.

## Dedicated Citizen Modules (`citizen/`):
- `home/`: Citizen local air quality glance, nearest sensor, health advisory.
- `map/`: Simplified citizen pollution map with search and navigation.
- `report/`: 1-tap camera capture, geolocation tagging, and submission flow.
- `insights/`: Vulnerability-aware personal health recommendations.
- `assistant/`: Conversational Gemini assistant for citizen air quality questions.
- `profile/`: Past citizen report tracking and local area bookmarks.
