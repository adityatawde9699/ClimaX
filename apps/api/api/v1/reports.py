"""
Reports API Router — /api/v1/reports
Boundary for citizen environmental reports and multimedia submissions.
Implementation scheduled for Phase 4.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from schemas.entities import CitizenReportCreate, CitizenReportRead
from schemas.base import ApiResponse, PaginatedResponse

router = APIRouter(prefix="/reports", tags=["Citizen Reports"])


@router.post("/", response_model=ApiResponse[CitizenReportRead], summary="Submit a citizen environmental report")
async def submit_citizen_report(report: CitizenReportCreate):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. Report ingestion implementation begins in Phase 4."
    )


@router.get("/", response_model=PaginatedResponse[CitizenReportRead], summary="List citizen reports")
async def list_citizen_reports():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. Implementation begins in Phase 4."
    )
