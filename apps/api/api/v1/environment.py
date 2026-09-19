"""
Environment API Router — /api/v1/environment
Boundary for atmospheric observations, AQI readings, and weather telemetry.
Implementation scheduled for Phase 3.
"""

from datetime import datetime
from uuid import uuid4

from events.broker import broker
from fastapi import APIRouter, Depends, Query
from repositories.alerts import AlertRepository
from security.jwt import require_roles
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.entities import EnvironmentalObservation
from schemas.base import ApiResponse, PaginatedResponse
from schemas.entities import EnvironmentalObservationCreate, EnvironmentalObservationRead
from services.alert_service import AlertService

router = APIRouter(prefix="/environment", tags=["Environment & Telemetry"])


@router.post("/observations", response_model=ApiResponse[EnvironmentalObservationRead])
async def create_observation(
    payload: EnvironmentalObservationCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_roles("AUTHORITY", "ADMIN")),
):
    observation = EnvironmentalObservation(id=str(uuid4()), **payload.model_dump())
    db.add(observation)
    alert = None
    if payload.pm25 is not None:
        alert = await AlertService(AlertRepository(db)).create_pm25_threshold_alert(
            sensor_id=payload.sensor_id,
            pm25=payload.pm25,
        )
    await db.commit()
    await db.refresh(observation)
    await broker.publish(
        "observation.ingested",
        {"id": observation.id, "sensor_id": observation.sensor_id, "aqi": observation.aqi},
    )
    if alert is not None:
        await broker.publish("alert.dispatched", {"id": alert.id, "severity": alert.severity})
    return ApiResponse(data=observation)


@router.get("/observations", response_model=PaginatedResponse[EnvironmentalObservationRead])
async def list_observations(
    sensor_id: str | None = None,
    from_timestamp: datetime | None = Query(default=None, alias="from"),
    to_timestamp: datetime | None = Query(default=None, alias="to"),
    limit: int = Query(100, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    statement = (
        select(EnvironmentalObservation)
        .order_by(desc(EnvironmentalObservation.timestamp))
        .limit(limit)
    )
    if sensor_id:
        statement = statement.where(EnvironmentalObservation.sensor_id == sensor_id)
    if from_timestamp:
        statement = statement.where(EnvironmentalObservation.timestamp >= from_timestamp)
    if to_timestamp:
        statement = statement.where(EnvironmentalObservation.timestamp <= to_timestamp)
    data = (await db.scalars(statement)).all()
    return PaginatedResponse(data=data, total=len(data), per_page=limit)


@router.get(
    "/latest",
    response_model=PaginatedResponse[EnvironmentalObservationRead],
    summary="Get latest environmental observations",
)
async def get_latest_observations(
    sensor_id: str | None = None,
    limit: int = Query(100, le=200),
    db: AsyncSession = Depends(get_db),
):
    statement = (
        select(EnvironmentalObservation)
        .order_by(desc(EnvironmentalObservation.timestamp))
        .limit(limit)
    )
    if sensor_id:
        statement = statement.where(EnvironmentalObservation.sensor_id == sensor_id)
    data = (await db.scalars(statement)).all()
    return PaginatedResponse(data=data, total=len(data), per_page=limit)
