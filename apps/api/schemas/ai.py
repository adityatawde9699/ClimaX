"""
ClimaX AI Schema Contracts & Trust Taxonomy
Compliant with 4-tier information classification: OBSERVED, INFERRED, PREDICTED, VERIFIED.
"""

from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, Field


class InformationTier(str, Enum):
    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    PREDICTED = "PREDICTED"
    VERIFIED = "VERIFIED"


class VerificationStatus(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    FIELD_VERIFIED = "FIELD_VERIFIED"
    REJECTED = "REJECTED"
    DISPUTED = "DISPUTED"


class ConfidenceTier(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class PollutionCategory(str, Enum):
    BIOMASS_BURNING = "BIOMASS_BURNING"
    INDUSTRIAL_EMISSION = "INDUSTRIAL_EMISSION"
    VEHICULAR_CONGESTION = "VEHICULAR_CONGESTION"
    CONSTRUCTION_DUST = "CONSTRUCTION_DUST"
    WASTE_INCINERATION = "WASTE_INCINERATION"
    BRICK_KILN = "BRICK_KILN"
    ROAD_DUST = "ROAD_DUST"
    FIRE_INCIDENT = "FIRE_INCIDENT"
    HAZARDOUS_CHEMICAL = "HAZARDOUS_CHEMICAL"
    OTHER = "OTHER"


class AIExplanationSchema(BaseModel):
    """Canonical contract required for all AI inferences and model predictions."""

    result: str = Field(..., description="Summary conclusion of the AI analysis")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Normalized confidence score [0.0 - 1.0]"
    )
    confidence_tier: ConfidenceTier = Field(..., description="Categorized confidence bracket")
    evidence: list[str] = Field(
        default_factory=list, description="Explicit observational or sensor justifications"
    )
    data_sources: list[str] = Field(
        default_factory=list, description="IDs or URIs of inputs feeding the inference"
    )
    model: str = Field(..., description="Model identifier and checkpoint version")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Timestamp of inference"
    )
    verification_status: VerificationStatus = Field(default=VerificationStatus.UNVERIFIED)
    reasoning_steps: list[str] = Field(default_factory=list)
    uncertainty_disclaimer: str = (
        "AI-generated assessment; verify with field evidence before enforcement."
    )
    pollution_category: PollutionCategory = PollutionCategory.OTHER
    suggested_severity: str = "MODERATE"
    plume_bbox: list[float] | None = Field(default=None, min_length=4, max_length=4)
    health_risk: str | None = None
