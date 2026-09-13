from datetime import UTC, datetime
from uuid import uuid4

from repositories.interventions import InterventionRepository

from models.entities import Intervention
from schemas.entities import InterventionCreate


class InterventionService:
    def __init__(self, repository: InterventionRepository):
        self.repository = repository

    async def dispatch(self, payload: InterventionCreate) -> Intervention:
        return await self.repository.create(
            {"id": str(uuid4()), **payload.model_dump(), "dispatched_at": datetime.now(UTC)}
        )

    async def update_status(self, intervention_id: str, status: str) -> Intervention | None:
        field = {"EXECUTED": "executed_at", "COMPLETED": "completed_at"}.get(status)
        if field is None:
            raise ValueError("Invalid intervention status")
        return await self.repository.update(intervention_id, {field: datetime.now(UTC)})
