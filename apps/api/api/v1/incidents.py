"""
Incidents API Router — /api/v1/incidents
Boundary for environmental incident triage, field dispatch, and status lifecycle.
Implementation scheduled for Phase 9.
"""

from fastapi import APIRouter, HTTPException, status
from schemas.entities import IncidentCreate, IncidentRead
from schemas.base import ApiResponse, PaginatedResponse

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.get("/", response_model=PaginatedResponse[IncidentRead], summary="List active incidents")
async def list_incidents():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. Incident management implementation begins in Phase 9."
    )


@router.post("/", response_model=ApiResponse[IncidentRead], summary="Create new incident")
async def create_incident(incident: IncidentCreate):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. Incident management implementation begins in Phase 9."
    )
