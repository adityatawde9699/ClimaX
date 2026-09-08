"""
ClimaX Telemetry & Observability Interfaces
Contract for collecting OpenTelemetry metrics, tracking AI model latency, and token expenditure.
"""

from abc import ABC, abstractmethod


class IMetricsCollector(ABC):
    @abstractmethod
    def record_ai_inference(self, model_name: str, latency_ms: float, token_count: int, success: bool) -> None:
        pass

    @abstractmethod
    def record_sensor_reading_ingested(self, sensor_type: str) -> None:
        pass

    @abstractmethod
    def record_incident_transition(self, from_status: str, to_status: str) -> None:
        pass
