"""
ClimaX Event Bus & Pub/Sub Interfaces
Contract for asynchronous event publishing and streaming message distribution.
"""

from abc import ABC, abstractmethod
from typing import Any


class IEventPublisher(ABC):
    """Publishes domain events to Cloud Pub/Sub or local message bus."""

    @abstractmethod
    async def publish_event(
        self, topic: str, message: dict[str, Any], attributes: dict[str, str]
    ) -> str:
        pass


class IEventSubscriber(ABC):
    """Subscribes to incoming event streams."""

    @abstractmethod
    async def subscribe(self, subscription_name: str, handler_callback: Any) -> None:
        pass
