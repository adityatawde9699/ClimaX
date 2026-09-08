"""
ClimaX Entity Request/Response Schemas
Defines the Pydantic DTO contracts for all 16 domain entities.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from schemas.ai import (
    AIExplanationSchema,
    InformationTier,
    PollutionCategory,
    VerificationStatus,
)
from schemas.base import CoordinatesDTO


class UserRole(str, Enum):
    CITIZEN = "CITIZEN"
    AUTHORITY = "AUTHORITY"
    RESEARCHER = "RESEARCHER"
    ADMIN = "ADMIN"


class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    DISPATCHED = "DISPATCHED"
    MITIGATED = "MITIGATED"
    RESOLVED = "RESOLVED"
    DISMISSED = "DISMISSED"


class IncidentSeverity(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"
    CRITICAL = "CRITICAL"


class AlertChannel(str, Enum):
    IN_APP = "IN_APP"
    SMS = "SMS"
    PUSH = "PUSH"
    EMAIL = "EMAIL"
    MUNICIPAL_BROADCAST = "MUNICIPAL_BROADCAST"


class SensorType(str, Enum):
    GOVERNMENT_STATION = "GOVERNMENT_STATION"
    IOT_LOW_COST = "IOT_LOW_COST"
    COMMUNITY = "COMMUNITY"
    SATELLITE_PIXEL = "SATELLITE_PIXEL"


# 1. User DTOs
class UserBase(BaseModel):
    email: str
    full_name: str
    role: UserRole = UserRole.CITIZEN
    organization_id: Optional[str] = None
    preferred_language: str = "en"


class UserRead(UserBase):
    id: str
    is_active: bool
    created_at: datetime


# 2. Organization DTOs
class OrganizationRead(BaseModel):
    id: str
    name: str
    jurisdiction_code: str
    department: str
    contact_email: str
    created_at: datetime


# 3. DataSource DTOs
class DataSourceRead(BaseModel):
    id: str
    name: str
    source_type: str
    provider: str
    refresh_interval_seconds: int
    is_active: bool
    created_at: datetime


# 4. Sensor DTOs
class SensorRead(BaseModel):
    id: str
    data_source_id: str
    external_sensor_id: str
    sensor_type: SensorType
    model_name: str
    location: CoordinatesDTO
    is_calibrated: bool
    is_active: bool
    last_ping_at: Optional[datetime] = None


# 5. EnvironmentalObservation DTOs
class EnvironmentalObservationCreate(BaseModel):
    sensor_id: str
    timestamp: datetime
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    no2: Optional[float] = None
    so2: Optional[float] = None
    co: Optional[float] = None
    o3: Optional[float] = None
    aqi: Optional[float] = None
    temperature_c: Optional[float] = None
    humidity_percent: Optional[float] = None
    wind_speed_kmh: Optional[float] = None
    wind_direction_deg: Optional[float] = None


class EnvironmentalObservationRead(EnvironmentalObservationCreate):
    id: str
    tier: InformationTier = InformationTier.OBSERVED
    created_at: datetime


# 6. CitizenReport DTOs
class CitizenReportCreate(BaseModel):
    location: CoordinatesDTO
    address_text: Optional[str] = None
    category: PollutionCategory
    description: str
    media_urls: List[str] = Field(default_factory=list)


class CitizenReportRead(BaseModel):
    id: str
    user_id: Optional[str] = None
    tier: InformationTier = InformationTier.OBSERVED
    location: CoordinatesDTO
    address_text: Optional[str] = None
    category: PollutionCategory
    description: str
    media_urls: List[str]
    status: str
    incident_id: Optional[str] = None
    created_at: datetime


# 7. AIAnalysis DTOs
class AIAnalysisRead(BaseModel):
    id: str
    report_id: Optional[str] = None
    observation_id: Optional[str] = None
    tier: InformationTier = InformationTier.INFERRED
    classification: PollutionCategory
    explanation: AIExplanationSchema
    suggested_severity: IncidentSeverity
    created_at: datetime


# 8. PollutionEvent DTOs
class PollutionEventRead(BaseModel):
    id: str
    event_type: str
    tier: InformationTier
    start_time: datetime
    end_time: Optional[datetime] = None
    peak_pm25: Optional[float] = None
    affected_radius_meters: float
    severity: IncidentSeverity
    created_at: datetime


# 9. Prediction DTOs
class PredictionRead(BaseModel):
    id: str
    sensor_id: Optional[str] = None
    target_location: CoordinatesDTO
    forecast_timestamp: datetime
    horizon_hours: int
    tier: InformationTier = InformationTier.PREDICTED
    predicted_pm25: float
    predicted_aqi: float
    confidence_interval_low: float
    confidence_interval_high: float
    explanation: AIExplanationSchema
    created_at: datetime


# 10. RiskAssessment DTOs
class RiskAssessmentRead(BaseModel):
    id: str
    location: CoordinatesDTO
    risk_score: float
    severity: IncidentSeverity
    population_vulnerability_index: float
    sensitive_receptors_count: int
    dominant_pollutant: str
    calculated_at: datetime


# 11. Alert DTOs
class AlertCreate(BaseModel):
    title: str
    message: str
    severity: IncidentSeverity
    channel: AlertChannel
    affected_radius_m: Optional[float] = None


class AlertRead(AlertCreate):
    id: str
    is_dispatched: bool
    dispatched_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    created_at: datetime


# 12. Incident DTOs
class IncidentCreate(BaseModel):
    title: str
    severity: IncidentSeverity
    category: PollutionCategory
    location: CoordinatesDTO
    assigned_officer_id: Optional[str] = None


class IncidentRead(IncidentCreate):
    id: str
    organization_id: str
    status: IncidentStatus
    risk_score: Optional[float] = None
    ai_analysis_id: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None


# 13. Verification DTOs
class VerificationCreate(BaseModel):
    incident_id: str
    status: VerificationStatus
    official_notes: str
    field_photos: List[str] = Field(default_factory=list)


class VerificationRead(VerificationCreate):
    id: str
    verified_by_user_id: str
    tier: InformationTier = InformationTier.VERIFIED
    verified_at: datetime


# 14. Intervention DTOs
class InterventionCreate(BaseModel):
    incident_id: str
    intervention_type: str
    executing_agency: str
    action_summary: str


class InterventionRead(InterventionCreate):
    id: str
    dispatched_at: datetime
    executed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


# 15. InterventionMeasurement DTOs
class InterventionMeasurementRead(BaseModel):
    id: str
    intervention_id: str
    pre_intervention_pm25: float
    post_intervention_pm25: float
    delta_pm25_percent: float
    evaluation_window_hours: int
    is_statistically_significant: bool
    measured_at: datetime


# 16. AuditLog DTOs
class AuditLogRead(BaseModel):
    id: str
    user_id: Optional[str] = None
    action: str
    entity_name: str
    entity_id: str
    ip_address: Optional[str] = None
    changes: Optional[Dict[str, Any]] = None
    timestamp: datetime
