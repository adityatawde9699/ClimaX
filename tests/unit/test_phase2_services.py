from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from schemas.entities import (
    AlertChannel,
    AlertCreate,
    IncidentSeverity,
    IncidentStatus,
    UserCreate,
    UserRole,
    UserUpdate,
)
from services.alert_service import AlertService
from services.incident_service import IncidentService, can_transition
from services.intervention_service import InterventionService
from services.observation_service import ObservationService
from services.report_service import ReportService
from services.sensor_service import SensorService
from services.user_service import UserService


def test_incident_state_machine_accepts_only_forward_transitions():
    assert can_transition("OPEN", "INVESTIGATING")
    assert can_transition("MITIGATED", "RESOLVED")
    assert not can_transition("RESOLVED", "INVESTIGATING")


@pytest.mark.asyncio
async def test_incident_service_rejects_invalid_transition():
    repository = SimpleNamespace(
        get=AsyncMock(return_value=SimpleNamespace(status="RESOLVED")), update=AsyncMock()
    )
    with pytest.raises(ValueError):
        await IncidentService(repository).transition("incident-1", "INVESTIGATING")
    repository.update.assert_not_awaited()


@pytest.mark.asyncio
async def test_incident_service_resolves_incident():
    incident = SimpleNamespace(status="MITIGATED")
    repository = SimpleNamespace(
        get=AsyncMock(return_value=incident), update=AsyncMock(return_value=incident)
    )
    await IncidentService(repository).transition("incident-1", IncidentStatus.RESOLVED.value)
    changes = repository.update.await_args.args[1]
    assert changes["status"] == "RESOLVED"
    assert "resolved_at" in changes


@pytest.mark.asyncio
async def test_report_status_validation():
    repository = SimpleNamespace(update=AsyncMock())
    service = ReportService(repository)
    with pytest.raises(ValueError):
        await service.update_status("report-1", "INVALID")
    await service.update_status("report-1", "TRIAGED")
    repository.update.assert_awaited_once_with("report-1", {"status": "TRIAGED"})


@pytest.mark.asyncio
async def test_intervention_status_validation():
    repository = SimpleNamespace(update=AsyncMock(return_value=object()))
    service = InterventionService(repository)
    with pytest.raises(ValueError):
        await service.update_status("intervention-1", "INVALID")
    await service.update_status("intervention-1", "COMPLETED")
    assert "completed_at" in repository.update.await_args.args[1]


@pytest.mark.asyncio
async def test_alert_service_dispatches_immediately():
    repository = SimpleNamespace(create=AsyncMock(return_value=object()))
    payload = AlertCreate(
        title="Smoke",
        message="Avoid exposure",
        severity=IncidentSeverity.HIGH,
        channel=AlertChannel.IN_APP,
    )
    await AlertService(repository).create_and_dispatch(payload)
    data = repository.create.await_args.args[0]
    assert data["is_dispatched"] is True
    assert data["severity"] == "HIGH"


@pytest.mark.asyncio
async def test_sensor_service_lists_and_records_ping():
    repository = SimpleNamespace(
        list=AsyncMock(return_value=[]), update=AsyncMock(return_value=object())
    )
    service = SensorService(repository)
    assert await service.list() == []
    await service.record_ping("sensor-1")
    assert repository.update.await_args.args[1]["is_active"] is True


@pytest.mark.asyncio
async def test_observation_service_ingests_batch():
    repository = SimpleNamespace(create=AsyncMock(return_value=object()))
    service = ObservationService(repository)
    from schemas.entities import EnvironmentalObservationCreate

    payload = EnvironmentalObservationCreate(
        sensor_id="sensor-1", timestamp="2026-01-01T00:00:00Z", pm25=42
    )
    assert len(await service.ingest_many([payload])) == 1
    assert repository.create.await_args.args[0]["sensor_id"] == "sensor-1"


@pytest.mark.asyncio
async def test_user_service_create_and_update():
    session = SimpleNamespace(scalar=AsyncMock(return_value=None))
    repository = SimpleNamespace(
        session=session,
        create=AsyncMock(return_value=object()),
        update=AsyncMock(return_value=object()),
    )
    service = UserService(repository)
    payload = UserCreate(
        email="citizen@example.com",
        full_name="Citizen",
        password="long-password",
        role=UserRole.CITIZEN,
    )
    await service.create(payload)
    created = repository.create.await_args.args[0]
    assert created["role"] == "CITIZEN" and created["password_hash"] != payload.password
    await service.update("user-1", UserUpdate(role=UserRole.AUTHORITY))
    repository.update.assert_awaited_with("user-1", {"role": "AUTHORITY"})
