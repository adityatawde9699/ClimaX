from datetime import datetime
from uuid import uuid4

from repositories.observations import ObservationRepository
from sqlalchemy import select

from models.entities import EnvironmentalObservation
from schemas.entities import EnvironmentalObservationCreate


class ObservationService:
    def __init__(self, repository: ObservationRepository):
        self.repository = repository

    async def ingest_many(
        self, payloads: list[EnvironmentalObservationCreate]
    ) -> list[EnvironmentalObservation]:
        return [
            await self.repository.create({"id": str(uuid4()), **item.model_dump()})
            for item in payloads
        ]

    async def query(
        self, sensor_id: str | None, start: datetime | None, end: datetime | None, limit: int = 100
    ):
        statement = (
            select(EnvironmentalObservation)
            .order_by(EnvironmentalObservation.timestamp.desc())
            .limit(limit)
        )
        if sensor_id:
            statement = statement.where(EnvironmentalObservation.sensor_id == sensor_id)
        if start:
            statement = statement.where(EnvironmentalObservation.timestamp >= start)
        if end:
            statement = statement.where(EnvironmentalObservation.timestamp <= end)
        return list((await self.repository.session.scalars(statement)).all())
