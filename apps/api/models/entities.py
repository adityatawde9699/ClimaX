"""
ClimaX ORM Entity Declarations
Outlines database tables, foreign keys, and PostGIS geometry columns for all 16 core entities.
No database connection or runtime migrations are executed in Phase 0.
"""

from datetime import datetime
from typing import Any

from geoalchemy2 import Geometry
from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    google_sub: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="CITIZEN")
    organization_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=True
    )
    preferred_language: Mapped[str] = mapped_column(String(10), default="en")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    jurisdiction_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    contact_email: Mapped[str] = mapped_column(String(255), nullable=False)


class DataSource(Base, TimestampMixin):
    __tablename__ = "data_sources"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    refresh_interval_seconds: Mapped[int] = mapped_column(Integer, default=300)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    meta_info: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class Sensor(Base, TimestampMixin):
    __tablename__ = "sensors"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    data_source_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("data_sources.id"), nullable=False
    )
    external_sensor_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    sensor_type: Mapped[str] = mapped_column(String(50), nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    geom = mapped_column(Geometry(geometry_type="POINT", srid=4326), nullable=False)
    is_calibrated: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_ping_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class EnvironmentalObservation(Base, TimestampMixin):
    __tablename__ = "environmental_observations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    sensor_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("sensors.id"), index=True, nullable=False
    )
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    tier: Mapped[str] = mapped_column(String(20), default="OBSERVED")
    quality_flag: Mapped[str] = mapped_column(String(20), default="VALID", nullable=False)
    pm25: Mapped[float | None] = mapped_column(Float, nullable=True)
    pm10: Mapped[float | None] = mapped_column(Float, nullable=True)
    no2: Mapped[float | None] = mapped_column(Float, nullable=True)
    so2: Mapped[float | None] = mapped_column(Float, nullable=True)
    co: Mapped[float | None] = mapped_column(Float, nullable=True)
    o3: Mapped[float | None] = mapped_column(Float, nullable=True)
    aqi: Mapped[float | None] = mapped_column(Float, nullable=True)
    temperature_c: Mapped[float | None] = mapped_column(Float, nullable=True)
    humidity_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    wind_speed_kmh: Mapped[float | None] = mapped_column(Float, nullable=True)
    wind_direction_deg: Mapped[float | None] = mapped_column(Float, nullable=True)


class CitizenReport(Base, TimestampMixin):
    __tablename__ = "citizen_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    tier: Mapped[str] = mapped_column(String(20), default="OBSERVED")
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    geom = mapped_column(Geometry(geometry_type="POINT", srid=4326), nullable=False)
    address_text: Mapped[str | None] = mapped_column(String(500), nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    media_urls: Mapped[list[str]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(30), default="SUBMITTED")
    incident_id: Mapped[str | None] = mapped_column(String(36), nullable=True)


class AIAnalysis(Base, TimestampMixin):
    __tablename__ = "ai_analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    report_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("citizen_reports.id"), nullable=True
    )
    observation_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("environmental_observations.id"), nullable=True
    )
    tier: Mapped[str] = mapped_column(String(20), default="INFERRED")
    classification: Mapped[str] = mapped_column(String(50), nullable=False)
    explanation: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    suggested_severity: Mapped[str] = mapped_column(String(30), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    raw_model_response: Mapped[str | None] = mapped_column(Text, nullable=True)


class PollutionEvent(Base, TimestampMixin):
    __tablename__ = "pollution_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    tier: Mapped[str] = mapped_column(String(20), default="INFERRED")
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    geom = mapped_column(Geometry(geometry_type="POLYGON", srid=4326), nullable=True)
    peak_pm25: Mapped[float | None] = mapped_column(Float, nullable=True)
    affected_radius_meters: Mapped[float] = mapped_column(Float, default=1000.0)
    severity: Mapped[str] = mapped_column(String(30), nullable=False)


class Prediction(Base, TimestampMixin):
    __tablename__ = "predictions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    sensor_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("sensors.id"), nullable=True
    )
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    forecast_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    horizon_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    tier: Mapped[str] = mapped_column(String(20), default="PREDICTED")
    predicted_pm25: Mapped[float] = mapped_column(Float, nullable=False)
    predicted_aqi: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_interval_low: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_interval_high: Mapped[float] = mapped_column(Float, nullable=False)
    explanation: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)


class RiskAssessment(Base, TimestampMixin):
    __tablename__ = "risk_assessments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[str] = mapped_column(String(30), nullable=False)
    population_vulnerability_index: Mapped[float] = mapped_column(Float, nullable=False)
    sensitive_receptors_count: Mapped[int] = mapped_column(Integer, default=0)
    dominant_pollutant: Mapped[str] = mapped_column(String(20), default="PM2.5")
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class Alert(Base, TimestampMixin):
    __tablename__ = "alerts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(30), nullable=False)
    channel: Mapped[str] = mapped_column(String(30), nullable=False)
    affected_radius_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_dispatched: Mapped[bool] = mapped_column(Boolean, default=False)
    dispatched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Incident(Base, TimestampMixin):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="OPEN")
    severity: Mapped[str] = mapped_column(String(30), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    geom = mapped_column(Geometry(geometry_type="POINT", srid=4326), nullable=False)
    assigned_officer_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=True
    )
    risk_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    ai_analysis_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("ai_analyses.id"), nullable=True
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    root_cause_summary: Mapped[str | None] = mapped_column(Text, nullable=True)


class Verification(Base, TimestampMixin):
    __tablename__ = "verifications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    incident_id: Mapped[str] = mapped_column(String(36), ForeignKey("incidents.id"), nullable=False)
    verified_by_user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    tier: Mapped[str] = mapped_column(String(20), default="VERIFIED")
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    official_notes: Mapped[str] = mapped_column(Text, nullable=False)
    field_photos: Mapped[list[str]] = mapped_column(JSON, default=list)
    verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class Intervention(Base, TimestampMixin):
    __tablename__ = "interventions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    incident_id: Mapped[str] = mapped_column(String(36), ForeignKey("incidents.id"), nullable=False)
    intervention_type: Mapped[str] = mapped_column(String(50), nullable=False)
    dispatched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    executed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    executing_agency: Mapped[str] = mapped_column(String(100), nullable=False)
    action_summary: Mapped[str] = mapped_column(Text, nullable=False)


class InterventionMeasurement(Base, TimestampMixin):
    __tablename__ = "intervention_measurements"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    intervention_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("interventions.id"), nullable=False
    )
    pre_intervention_pm25: Mapped[float] = mapped_column(Float, nullable=False)
    post_intervention_pm25: Mapped[float] = mapped_column(Float, nullable=False)
    delta_pm25_percent: Mapped[float] = mapped_column(Float, nullable=False)
    evaluation_window_hours: Mapped[int] = mapped_column(Integer, default=6)
    is_statistically_significant: Mapped[bool] = mapped_column(Boolean, default=False)
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_name: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    changes: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
