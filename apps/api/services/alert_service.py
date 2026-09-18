from datetime import UTC, datetime
from uuid import uuid4

from repositories.alerts import AlertRepository

from models.entities import Alert
from schemas.entities import AlertCreate


class AlertService:
    def __init__(self, repository: AlertRepository):
        self.repository = repository

    async def create_and_dispatch(self, payload: AlertCreate) -> Alert:
        data = payload.model_dump()
        data.update(
            id=str(uuid4()),
            severity=payload.severity.value,
            channel=payload.channel.value,
            is_dispatched=True,
            dispatched_at=datetime.now(UTC),
        )
        return await self.repository.create(data)

    async def dispatch(self, alert_id: str) -> Alert | None:
        return await self.repository.update(
            alert_id,
            {"is_dispatched": True, "dispatched_at": datetime.now(UTC)},
        )

    @staticmethod
    def severity_for_pm25(pm25: float) -> str | None:
        if pm25 > 250:
            return "CRITICAL"
        if pm25 > 150:
            return "VERY_HIGH"
        return None
