"""
ClimaX Background Task & Worker Interfaces
Contract for scheduled jobs, sensor ingestion, and async AI inference queues.
"""

from abc import ABC, abstractmethod


class IBackgroundWorker(ABC):
    """Background task executor interface."""

    @abstractmethod
    async def process_report_multimodal_queue(self) -> None:
        pass

    @abstractmethod
    async def ingest_external_sensors_job(self) -> None:
        pass

    @abstractmethod
    async def compute_hourly_risk_index_job(self) -> None:
        pass
