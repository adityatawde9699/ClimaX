"""Marks queued alerts dispatched; delivery providers plug in by channel."""

import json
from datetime import UTC, datetime

from events.broker import broker

from models.entities import Alert


class AlertDispatchWorker:
    async def process(self, raw_message: bytes, session) -> bool:
        payload = json.loads(raw_message)
        alert = await session.get(Alert, payload.get("alert_id"))
        if alert is None:
            return False
        alert.is_dispatched = True
        alert.dispatched_at = datetime.now(UTC)
        await session.commit()
        await broker.publish("alert.dispatched", {"id": alert.id, "severity": alert.severity})
        return True
