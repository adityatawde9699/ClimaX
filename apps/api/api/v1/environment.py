"""
Environment API Router — /api/v1/environment
Boundary for atmospheric observations, AQI readings, and weather telemetry.
Implementation scheduled for Phase 3.
"""

from fastapi import APIRouter, HTTPException, status
from schemas.entities import EnvironmentalObservationRead
from schemas.base import ApiResponse, PaginatedResponse, SpatialQueryFilter

router = APIRouter(prefix="/environment", tags=["Environment & Telemetry"])


@router.get("/latest", response_model=PaginatedResponse[EnvironmentalObservationRead], summary="Get latest environmental observations")
async def get_latest_observations(filters: SpatialQueryFilter):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. Environmental telemetry implementation begins in Phase 3."
    )
