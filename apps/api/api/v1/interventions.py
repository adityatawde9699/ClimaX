"""
Interventions API Router — /api/v1/interventions
Boundary for municipal pollution interventions and pre/post impact delta tracking.
Implementation scheduled for Phase 11.
"""

from fastapi import APIRouter, HTTPException, status
from schemas.entities import InterventionCreate, InterventionRead, InterventionMeasurementRead
from schemas.base import ApiResponse, PaginatedResponse

router = APIRouter(prefix="/interventions", tags=["Interventions & Impact"])


@router.post("/", response_model=ApiResponse[InterventionRead], summary="Record a municipal intervention")
async def record_intervention(intervention: InterventionCreate):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. Intervention tracking implementation begins in Phase 11."
    )


@router.get("/{intervention_id}/impact", response_model=ApiResponse[InterventionMeasurementRead], summary="Get measured intervention impact delta")
async def get_intervention_impact(intervention_id: str):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. Impact measurement implementation begins in Phase 11."
    )
