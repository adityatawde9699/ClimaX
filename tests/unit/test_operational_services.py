from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from core.config import settings
from services.alert_service import AlertService
from services.base import BaseService
from services.measurement_service import MeasurementService
from services.observation_service import ObservationService
from services.prediction_service import PredictionService
from services.risk_service import RiskService


def test_base_service_keeps_repository():
    repository = object()
    assert BaseService(repository).repository is repository


@pytest.mark.asyncio
async def test_threshold_alert_is_created_and_deduplicated():
    session = SimpleNamespace(scalar=AsyncMock(side_effect=[None, object()]))
    repository = SimpleNamespace(
        session=session,
        create=AsyncMock(return_value=SimpleNamespace(id="alert-1", severity="VERY_HIGH")),
    )
    service = AlertService(repository)
    created = await service.create_pm25_threshold_alert(sensor_id="sensor-1", pm25=180)
    duplicate = await service.create_pm25_threshold_alert(sensor_id="sensor-1", pm25=180)
    assert created.id == "alert-1"
    assert duplicate is None
    data = repository.create.await_args.args[0]
    assert data["severity"] == "VERY_HIGH"
    assert data["expires_at"] > data["dispatched_at"]
    assert await service.create_pm25_threshold_alert(sensor_id="sensor-1", pm25=100) is None


@pytest.mark.asyncio
async def test_observation_query_applies_filters():
    result = SimpleNamespace(all=lambda: ["reading"])
    session = SimpleNamespace(scalars=AsyncMock(return_value=result))
    repository = SimpleNamespace(session=session)
    service = ObservationService(repository)
    now = datetime.now(UTC)
    assert await service.query("sensor-1", now, now, limit=10) == ["reading"]
    session.scalars.assert_awaited_once()


@pytest.mark.asyncio
async def test_prediction_service_persists_provider_output():
    repository = SimpleNamespace(create=AsyncMock(side_effect=lambda data: data))
    service = PredictionService(repository)
    service.vertex.query_plume_prediction = AsyncMock(
        return_value={
            "latitude": 28.6,
            "longitude": 77.2,
            "forecast_timestamp": datetime.now(UTC),
            "horizon_hours": 24,
            "predicted_pm25": 90.0,
            "predicted_aqi": 160.0,
            "confidence_interval_low": 140.0,
            "confidence_interval_high": 180.0,
            "explanation": {"source": "test"},
        }
    )
    forecasts = await service.generate_forecast(28.6, 77.2, [24])
    assert forecasts[0]["tier"] == "PREDICTED"
    assert forecasts[0]["horizon_hours"] == 24

    service.vertex.query_plume_prediction = AsyncMock(side_effect=RuntimeError("offline"))
    with pytest.raises(RuntimeError, match="provider is unavailable"):
        await service.generate_forecast(28.6, 77.2, [6])


@pytest.mark.asyncio
async def test_measurement_uses_real_pre_and_post_observations():
    session = SimpleNamespace(
        scalar=AsyncMock(side_effect=[100.0, 80.0]),
        add=Mock(),
        commit=AsyncMock(),
        refresh=AsyncMock(),
    )
    intervention = SimpleNamespace(id="intervention-1", dispatched_at=datetime.now(UTC))
    measurement = await MeasurementService().record_from_observations(session, intervention)
    assert measurement is not None
    assert measurement.delta_pm25_percent == -20.0
    assert measurement.is_statistically_significant is True


@pytest.mark.asyncio
async def test_risk_evaluation_creates_incident_when_configured(monkeypatch):
    organization_id = "organization-1"
    monkeypatch.setattr(settings, "RISK_AUTO_INCIDENT_ORGANIZATION_ID", organization_id)
    session = SimpleNamespace(
        add=Mock(),
        get=AsyncMock(return_value=object()),
        scalar=AsyncMock(return_value=None),
        flush=AsyncMock(),
        commit=AsyncMock(),
        refresh=AsyncMock(),
    )
    publish = AsyncMock()
    monkeypatch.setattr("services.risk_service.broker.publish", publish)
    assessment = await RiskService().evaluate(
        session,
        latitude=28.6,
        longitude=77.2,
        aqi=500,
        receptors=10,
        population_density=1,
    )
    assert assessment.severity == "CRITICAL"
    assert session.add.call_count == 2
    publish.assert_awaited_once()
