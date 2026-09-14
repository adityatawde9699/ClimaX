"""Pub/Sub message handler for validated sensor observations.

The transport is intentionally injected so it runs with Google Pub/Sub in deployment and
can be unit-tested locally without cloud credentials.
"""

import asyncio
import json
from collections.abc import Awaitable, Callable
from uuid import uuid4

from pydantic import ValidationError
from repositories.observations import ObservationRepository
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from schemas.entities import EnvironmentalObservationCreate
from services.data_quality_service import DataQualityService

DeadLetter = Callable[[bytes, str], Awaitable[None]]


class SensorIngestWorker:
    concurrency = 10

    def __init__(self, dead_letter: DeadLetter | None = None):
        self.dead_letter = dead_letter
        self.observations_ingested_total = 0
        self.quality = DataQualityService()
        try:
            from prometheus_client import Counter

            self.metric = Counter(
                "sensor_observations_ingested_total",
                "Validated sensor observations written to the database",
            )
        except ImportError:
            self.metric = None

    async def process(self, raw_message: bytes, session: AsyncSession) -> bool:
        try:
            payload = json.loads(raw_message)
            observation = EnvironmentalObservationCreate.model_validate(payload)
            if not any(
                getattr(observation, field) is not None
                for field in ("pm25", "pm10", "no2", "so2", "co", "o3", "aqi")
            ):
                raise ValueError("at least one pollutant reading is required")
            record = observation.model_dump()
            record["id"] = str(uuid4())
            record["quality_flag"] = self.quality.validate(observation)
            await ObservationRepository(session).create(record)
            await session.commit()
            self.observations_ingested_total += 1
            if self.metric:
                self.metric.inc()
            return True
        except (ValueError, ValidationError, json.JSONDecodeError) as exc:
            await session.rollback()
            if self.dead_letter:
                await self.dead_letter(raw_message, str(exc))
            return False

    def subscribe(self, session_factory, subscription_name: str | None = None) -> None:
        """Run a Google Pub/Sub pull subscription until the process stops."""
        try:
            from google.cloud import pubsub_v1
        except ImportError as exc:
            raise RuntimeError("google-cloud-pubsub must be installed to subscribe") from exc

        subscriber = pubsub_v1.SubscriberClient()
        subscription = subscriber.subscription_path(
            settings.GCP_PROJECT_ID, subscription_name or settings.PUBSUB_SENSOR_SUBSCRIPTION
        )

        def callback(message) -> None:
            async def persist() -> bool:
                async with session_factory() as session:
                    return await self.process(message.data, session)

            if asyncio.run(persist()):
                message.ack()
            else:
                message.nack()

        subscriber.subscribe(subscription, callback=callback).result()
