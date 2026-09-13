"""Incident lifecycle rules used by Phase 2 routes."""

from datetime import UTC, datetime

from repositories.incidents import IncidentRepository

from models.entities import Incident
from schemas.entities import IncidentStatus

TRANSITIONS = {
    IncidentStatus.OPEN: {IncidentStatus.INVESTIGATING, IncidentStatus.DISMISSED},
    IncidentStatus.INVESTIGATING: {IncidentStatus.DISPATCHED, IncidentStatus.DISMISSED},
    IncidentStatus.DISPATCHED: {IncidentStatus.MITIGATED},
    IncidentStatus.MITIGATED: {IncidentStatus.RESOLVED},
    IncidentStatus.RESOLVED: set(),
    IncidentStatus.DISMISSED: set(),
}


def can_transition(current: str, target: str) -> bool:
    return IncidentStatus(target) in TRANSITIONS[IncidentStatus(current)]


class IncidentService:
    def __init__(self, repository: IncidentRepository):
        self.repository = repository

    async def transition(self, incident_id: str, target: str) -> Incident | None:
        incident = await self.repository.get(incident_id)
        if incident is None:
            return None
        if not can_transition(incident.status, target):
            raise ValueError(f"Invalid transition from {incident.status} to {target}")
        changes = {"status": target}
        if target == IncidentStatus.RESOLVED.value:
            changes["resolved_at"] = datetime.now(UTC)
        return await self.repository.update(incident_id, changes)
