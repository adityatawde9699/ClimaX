"""
Sensors API Router — /api/v1/sensors
Boundary for physical IoT sensor registries, calibration metadata, and ping telemetry.
Implementation scheduled for Phase 3.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.entities import Sensor
from schemas.base import PaginatedResponse
from schemas.entities import SensorRead

router = APIRouter(prefix="/sensors", tags=["Sensors"])


def serialize(sensor: Sensor) -> dict:
    return {
        "id": sensor.id,
        "data_source_id": sensor.data_source_id,
        "external_sensor_id": sensor.external_sensor_id,
        "sensor_type": sensor.sensor_type,
        "model_name": sensor.model_name,
        "location": {"latitude": sensor.latitude, "longitude": sensor.longitude},
        "is_calibrated": sensor.is_calibrated,
        "is_active": sensor.is_active,
        "last_ping_at": sensor.last_ping_at,
    }


@router.get("/", response_model=PaginatedResponse[SensorRead], summary="List registered sensors")
async def list_sensors(
    skip: int = 0, limit: int = Query(100, le=200), db: AsyncSession = Depends(get_db)
):
    total = await db.scalar(select(func.count()).select_from(Sensor)) or 0
    sensors = (await db.scalars(select(Sensor).offset(skip).limit(limit))).all()
    return PaginatedResponse(
        data=[serialize(sensor) for sensor in sensors],
        total=total,
        page=skip // limit + 1,
        per_page=limit,
        total_pages=max(1, (total + limit - 1) // limit),
    )


@router.get("/nearby", response_model=PaginatedResponse[SensorRead])
async def nearby_sensors(
    lat: float,
    lng: float,
    radius_m: float = Query(5000, gt=0, le=100000),
    db: AsyncSession = Depends(get_db),
):
    point = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)
    statement = (
        select(Sensor)
        .where(func.ST_DWithin(func.Geography(Sensor.geom), func.Geography(point), radius_m))
        .limit(200)
    )
    sensors = (await db.scalars(statement)).all()
    return PaginatedResponse(
        data=[serialize(sensor) for sensor in sensors], total=len(sensors), per_page=200
    )


@router.get("/{sensor_id}", response_model=SensorRead)
async def get_sensor(sensor_id: str, db: AsyncSession = Depends(get_db)):
    sensor = await db.get(Sensor, sensor_id)
    if sensor is None:
        raise HTTPException(404, "Sensor not found")
    return serialize(sensor)
