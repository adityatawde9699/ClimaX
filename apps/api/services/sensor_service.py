from datetime import UTC, datetime

from repositories.sensors import SensorRepository

from models.entities import Sensor


class SensorService:
    def __init__(self, repository: SensorRepository):
        self.repository = repository

    async def list(self, skip: int = 0, limit: int = 100) -> list[Sensor]:
        return await self.repository.list(skip, limit)

    async def record_ping(self, sensor_id: str) -> Sensor | None:
        return await self.repository.update(
            sensor_id, {"last_ping_at": datetime.now(UTC), "is_active": True}
        )
