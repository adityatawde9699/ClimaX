"""
Alerts API Router — /api/v1/alerts
Boundary for public environmental advisories and automated threshold alerts.
Implementation scheduled for Phase 9.
"""

from fastapi import APIRouter, HTTPException, status
from schemas.entities import AlertCreate, AlertRead
from schemas.base import ApiResponse, PaginatedResponse

router = APIRouter(prefix="/alerts", tags=["Alerts & Advisories"])


@router.get("/", response_model=PaginatedResponse[AlertRead], summary="List active environmental alerts")
async def list_alerts():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. Alert management implementation begins in Phase 9."
    )


@router.post("/", response_model=ApiResponse[AlertRead], summary="Broadcast new alert")
async def broadcast_alert(alert: AlertCreate):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. Alert management implementation begins in Phase 9."
    )
