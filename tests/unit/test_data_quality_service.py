from datetime import UTC, datetime

from schemas.entities import EnvironmentalObservationCreate
from services.data_quality_service import DataQualityService


def observation(pm25: float | None) -> EnvironmentalObservationCreate:
    return EnvironmentalObservationCreate(
        sensor_id="sensor-1", timestamp=datetime.now(UTC), pm25=pm25
    )


def test_pm25_outliers_are_suspect():
    service = DataQualityService()
    assert service.validate(observation(501)) == "SUSPECT"
    assert service.validate(observation(-1)) == "SUSPECT"
    assert service.validate(observation(120)) == "VALID"


def test_nearby_consistency_tolerates_missing_or_normal_values():
    service = DataQualityService()
    assert service.is_consistent_with_nearby(None, [80, 100, 120])
    assert service.is_consistent_with_nearby(130, [90, 100, 110])
    assert not service.is_consistent_with_nearby(600, [90, 100, 110])
