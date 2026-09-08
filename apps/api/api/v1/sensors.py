"""
Sensors API Router — /api/v1/sensors
Boundary for physical IoT sensor registries, calibration metadata, and ping telemetry.
Implementation scheduled for Phase 3.
"""

from fastapi import APIRouter, HTTPException, status
from schemas.entities import SensorRead
from schemas.base import ApiResponse, PaginatedResponse

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.get("/", response_model=PaginatedResponse[SensorRead], summary="List registered sensors")
async def list_sensors():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. Sensor registry implementation begins in Phase 3."
    )
