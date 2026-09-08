-- ==============================================================================
-- ClimaX Google Cloud BigQuery Historical Data Warehouse Schemas
-- Partitioned and clustered for cost-effective longitudinal analytics
-- ==============================================================================

CREATE SCHEMA IF NOT EXISTS `climax-prod.climax_environmental_raw`
OPTIONS (
  location = "US"
);

-- Time-partitioned raw sensor observations table
CREATE TABLE IF NOT EXISTS `climax-prod.climax_environmental_raw.sensor_observations_partitioned`
(
  observation_id STRING NOT NULL,
  sensor_id STRING NOT NULL,
  data_source_id STRING NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  tier STRING NOT NULL,
  pm25 FLOAT64,
  pm10 FLOAT64,
  no2 FLOAT64,
  so2 FLOAT64,
  co FLOAT64,
  o3 FLOAT64,
  aqi FLOAT64,
  latitude FLOAT64 NOT NULL,
  longitude FLOAT64 NOT NULL,
  temperature_c FLOAT64,
  humidity_percent FLOAT64,
  wind_speed_kmh FLOAT64,
  wind_direction_deg FLOAT64,
  ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(timestamp)
CLUSTER BY sensor_id, tier;
