# Environmental Data Ingestion Service (`services/environmental-data`)

Responsible for continuous streaming and batch ingestion of multi-source environmental telemetry.

## Responsibilities:
- **IoT Low-Cost Sensor Ingestion**: MQTT / HTTP webhook ingest for community and municipal sensor networks (PM2.5, PM10, temperature, humidity).
- **Government Open Data Connectors**: Connectors for OpenAQ, CPCB (India), EPA AirNow (US), and European EEA feeds.
- **Meteorological Data Feeds**: Real-time and forecasted wind velocity, relative humidity, pressure, and boundary layer height via OpenWeather / ECMWF.
- **Deduplication & Anomaly Cleansing**: Identifies stuck sensors, extreme physical outliers, and negative values before writing to PostgreSQL / PostGIS.

## Planned Implementation Phase:
- Phase 3 (Environmental Data Ingestion).
