"""
Reports API Router — /api/v1/reports
Boundary for citizen environmental reports and multimedia submissions.
Implementation scheduled for Phase 4.
"""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from security.jwt import get_current_user
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.entities import CitizenReport, User
from schemas.base import ApiResponse, PaginatedResponse
from schemas.entities import CitizenReportCreate, CitizenReportRead

router = APIRouter(prefix="/reports", tags=["Citizen Reports"])


def serialize_report(item: CitizenReport) -> dict:
    return {
        "id": item.id,
        "user_id": item.user_id,
        "tier": item.tier,
        "location": {"latitude": item.latitude, "longitude": item.longitude},
        "address_text": item.address_text,
        "category": item.category,
        "description": item.description,
        "media_urls": item.media_urls,
        "status": item.status,
        "incident_id": item.incident_id,
        "created_at": item.created_at,
    }


@router.post(
    "/",
    response_model=ApiResponse[CitizenReportRead],
    summary="Submit a citizen environmental report",
)
async def submit_citizen_report(
    report: CitizenReportCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    item = CitizenReport(
        id=str(uuid4()),
        user_id=user.id,
        latitude=report.location.latitude,
        longitude=report.location.longitude,
        geom=f"SRID=4326;POINT({report.location.longitude} {report.location.latitude})",
        address_text=report.address_text,
        category=report.category.value,
        description=report.description,
        media_urls=report.media_urls,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return ApiResponse(data=serialize_report(item))


@router.get(
    "/", response_model=PaginatedResponse[CitizenReportRead], summary="List citizen reports"
)
async def list_citizen_reports(
    status: str | None = None,
    bbox: str | None = Query(default=None, description="west,south,east,north"),
    db: AsyncSession = Depends(get_db),
):
    statement = select(CitizenReport)
    if status:
        statement = statement.where(CitizenReport.status == status)
    if bbox:
        try:
            west, south, east, north = (float(value) for value in bbox.split(","))
        except ValueError as error:
            raise HTTPException(422, "bbox must be west,south,east,north") from error
        envelope = func.ST_MakeEnvelope(west, south, east, north, 4326)
        statement = statement.where(func.ST_Intersects(CitizenReport.geom, envelope))
    items = (await db.scalars(statement)).all()
    data = [serialize_report(item) for item in items]
    return PaginatedResponse(data=data, total=len(data))


@router.get(
    "/{report_id}", response_model=ApiResponse[CitizenReportRead], summary="Get a citizen report"
)
async def get_citizen_report(report_id: str, db: AsyncSession = Depends(get_db)):
    item = await db.get(CitizenReport, report_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Citizen report not found")
    return ApiResponse(data=serialize_report(item))
