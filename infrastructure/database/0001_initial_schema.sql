-- ==============================================================================
-- ClimaX Initial Relational & Spatial Database Schema (PostgreSQL 16 + PostGIS)
-- ==============================================================================

-- 1. Enable PostGIS extension for spatial queries
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Organizations
CREATE TABLE IF NOT EXISTS organizations (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    jurisdiction_code VARCHAR(50) UNIQUE NOT NULL,
    department VARCHAR(100) NOT NULL,
    contact_email VARCHAR(255) NOT NULL,
    boundary_geojson JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Users
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'CITIZEN',
    organization_id VARCHAR(36) REFERENCES organizations(id) ON DELETE SET NULL,
    preferred_language VARCHAR(10) DEFAULT 'en',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Data Sources
CREATE TABLE IF NOT EXISTS data_sources (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    provider VARCHAR(100) NOT NULL,
    refresh_interval_seconds INTEGER DEFAULT 300,
    is_active BOOLEAN DEFAULT TRUE,
    meta_info JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Sensors
CREATE TABLE IF NOT EXISTS sensors (
    id VARCHAR(36) PRIMARY KEY,
    data_source_id VARCHAR(36) REFERENCES data_sources(id) ON DELETE CASCADE,
    external_sensor_id VARCHAR(100) NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    geom GEOMETRY(Point, 4326) NOT NULL,
    elevation_m DOUBLE PRECISION,
    is_calibrated BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    last_ping_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_sensors_geom ON sensors USING GIST (geom);

-- 6. Environmental Observations
CREATE TABLE IF NOT EXISTS environmental_observations (
    id VARCHAR(36) PRIMARY KEY,
    sensor_id VARCHAR(36) REFERENCES sensors(id) ON DELETE CASCADE,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    tier VARCHAR(20) DEFAULT 'OBSERVED',
    pm25 DOUBLE PRECISION,
    pm10 DOUBLE PRECISION,
    no2 DOUBLE PRECISION,
    so2 DOUBLE PRECISION,
    co DOUBLE PRECISION,
    o3 DOUBLE PRECISION,
    aqi DOUBLE PRECISION,
    temperature_c DOUBLE PRECISION,
    humidity_percent DOUBLE PRECISION,
    wind_speed_kmh DOUBLE PRECISION,
    wind_direction_deg DOUBLE PRECISION,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_obs_sensor_timestamp ON environmental_observations(sensor_id, timestamp DESC);

-- 7. Citizen Reports
CREATE TABLE IF NOT EXISTS citizen_reports (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    tier VARCHAR(20) DEFAULT 'OBSERVED',
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    geom GEOMETRY(Point, 4326) NOT NULL,
    address_text VARCHAR(500),
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    media_urls JSONB DEFAULT '[]'::jsonb,
    status VARCHAR(30) DEFAULT 'SUBMITTED',
    incident_id VARCHAR(36),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_citizen_reports_geom ON citizen_reports USING GIST (geom);

-- 8. AI Analyses
CREATE TABLE IF NOT EXISTS ai_analyses (
    id VARCHAR(36) PRIMARY KEY,
    report_id VARCHAR(36) REFERENCES citizen_reports(id) ON DELETE CASCADE,
    observation_id VARCHAR(36) REFERENCES environmental_observations(id) ON DELETE SET NULL,
    tier VARCHAR(20) DEFAULT 'INFERRED',
    classification VARCHAR(50) NOT NULL,
    explanation JSONB NOT NULL,
    suggested_severity VARCHAR(30) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. Incidents
CREATE TABLE IF NOT EXISTS incidents (
    id VARCHAR(36) PRIMARY KEY,
    organization_id VARCHAR(36) REFERENCES organizations(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(30) DEFAULT 'OPEN',
    severity VARCHAR(30) NOT NULL,
    category VARCHAR(50) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    geom GEOMETRY(Point, 4326) NOT NULL,
    assigned_officer_id VARCHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    risk_score DOUBLE PRECISION,
    ai_analysis_id VARCHAR(36) REFERENCES ai_analyses(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS idx_incidents_geom ON incidents USING GIST (geom);

-- 10. Pollution Events
CREATE TABLE IF NOT EXISTS pollution_events (
    id VARCHAR(36) PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    tier VARCHAR(20) DEFAULT 'INFERRED',
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    geom GEOMETRY(Polygon, 4326),
    peak_pm25 DOUBLE PRECISION,
    affected_radius_meters DOUBLE PRECISION DEFAULT 1000.0,
    severity VARCHAR(30) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 11. Predictions
CREATE TABLE IF NOT EXISTS predictions (
    id VARCHAR(36) PRIMARY KEY,
    sensor_id VARCHAR(36) REFERENCES sensors(id) ON DELETE SET NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    forecast_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    horizon_hours INTEGER NOT NULL,
    tier VARCHAR(20) DEFAULT 'PREDICTED',
    predicted_pm25 DOUBLE PRECISION NOT NULL,
    predicted_aqi DOUBLE PRECISION NOT NULL,
    confidence_interval_low DOUBLE PRECISION NOT NULL,
    confidence_interval_high DOUBLE PRECISION NOT NULL,
    explanation JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 12. Risk Assessments
CREATE TABLE IF NOT EXISTS risk_assessments (
    id VARCHAR(36) PRIMARY KEY,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    risk_score DOUBLE PRECISION NOT NULL,
    severity VARCHAR(30) NOT NULL,
    population_vulnerability_index DOUBLE PRECISION NOT NULL,
    sensitive_receptors_count INTEGER DEFAULT 0,
    dominant_pollutant VARCHAR(20) DEFAULT 'PM2.5',
    calculated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 13. Alerts
CREATE TABLE IF NOT EXISTS alerts (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    severity VARCHAR(30) NOT NULL,
    channel VARCHAR(30) NOT NULL,
    affected_radius_m DOUBLE PRECISION,
    is_dispatched BOOLEAN DEFAULT FALSE,
    dispatched_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 14. Verifications
CREATE TABLE IF NOT EXISTS verifications (
    id VARCHAR(36) PRIMARY KEY,
    incident_id VARCHAR(36) REFERENCES incidents(id) ON DELETE CASCADE,
    verified_by_user_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
    tier VARCHAR(20) DEFAULT 'VERIFIED',
    status VARCHAR(30) NOT NULL,
    official_notes TEXT NOT NULL,
    field_photos JSONB DEFAULT '[]'::jsonb,
    verified_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 15. Interventions
CREATE TABLE IF NOT EXISTS interventions (
    id VARCHAR(36) PRIMARY KEY,
    incident_id VARCHAR(36) REFERENCES incidents(id) ON DELETE CASCADE,
    intervention_type VARCHAR(50) NOT NULL,
    dispatched_at TIMESTAMP WITH TIME ZONE NOT NULL,
    executed_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    executing_agency VARCHAR(100) NOT NULL,
    action_summary TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 16. Intervention Measurements
CREATE TABLE IF NOT EXISTS intervention_measurements (
    id VARCHAR(36) PRIMARY KEY,
    intervention_id VARCHAR(36) REFERENCES interventions(id) ON DELETE CASCADE,
    pre_intervention_pm25 DOUBLE PRECISION NOT NULL,
    post_intervention_pm25 DOUBLE PRECISION NOT NULL,
    delta_pm25_percent DOUBLE PRECISION NOT NULL,
    evaluation_window_hours INTEGER DEFAULT 6,
    is_statistically_significant BOOLEAN DEFAULT FALSE,
    measured_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 17. Audit Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    action VARCHAR(100) NOT NULL,
    entity_name VARCHAR(100) NOT NULL,
    entity_id VARCHAR(36) NOT NULL,
    ip_address VARCHAR(45),
    changes JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_logs(entity_name, entity_id);
