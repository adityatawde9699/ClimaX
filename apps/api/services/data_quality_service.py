"""Validation rules for direct environmental observations."""

from schemas.entities import EnvironmentalObservationCreate


class DataQualityService:
    def is_suspect(self, observation: EnvironmentalObservationCreate) -> bool:
        return observation.pm25 is not None and not 0 <= observation.pm25 <= 500

    def validate(self, observation: EnvironmentalObservationCreate) -> str:
        return "SUSPECT" if self.is_suspect(observation) else "VALID"

    def is_consistent_with_nearby(
        self, reading: float | None, nearby_readings: list[float]
    ) -> bool:
        """Reject readings more than 3x away from the nearby median.

        The worker may call this once its spatial neighbour lookup has supplied
        observations from sensors inside the one-kilometre radius.
        """
        if reading is None or not nearby_readings:
            return True
        ordered = sorted(nearby_readings)
        median = ordered[len(ordered) // 2]
        return median == 0 or abs(reading - median) <= max(25.0, median * 3)
