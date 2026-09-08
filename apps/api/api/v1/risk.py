"""
Risk Engine API Router — /api/v1/risk
Boundary for multi-criteria environmental risk calculation and demographic vulnerability.
Implementation scheduled for Phase 8.
"""

from fastapi import APIRouter, HTTPException, status
from schemas.entities import RiskAssessmentRead
from schemas.base import ApiResponse, CoordinatesDTO

router = APIRouter(prefix="/risk", tags=["Environmental Risk"])


@router.post("/evaluate", response_model=ApiResponse[RiskAssessmentRead], summary="Evaluate risk score for target area")
async def evaluate_risk(location: CoordinatesDTO):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. Risk engine implementation begins in Phase 8."
    )
