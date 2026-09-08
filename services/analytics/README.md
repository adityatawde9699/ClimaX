# Analytics Domain Service (`services/analytics`)

Responsible for BigQuery analytical pipelines, historical trend aggregations, and open data export.

## Responsibilities:
- **BigQuery Historical Warehouse Sync**: Streams streaming raw observations and audit events into BigQuery partitioned tables.
- **Ward-by-Ward Environmental Scorecards**: Computes daily, weekly, and seasonal pollution exposure statistics by municipal ward.
- **Intervention Efficacy Analytics**: Measures statistical significance of air quality changes before and after city interventions (e.g. anti-smog guns, traffic bans).
- **Researcher Export Studio**: Generates formatted data bundles in GeoJSON, Parquet, and NetCDF formats for climate researchers.

## Planned Implementation Phase:
- Phase 3 (Data Pipelines), Phase 11 (Intervention Tracking), and Phase 13 (Hardening).
