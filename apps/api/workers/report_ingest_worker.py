"""Report ingestion handoff from Pub/Sub to the Phase 5 AI queue."""

import json
from collections.abc import Awaitable, Callable

from integrations.gcs_adapter import GCSAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from models.entities import CitizenReport

Publish = Callable[[str, bytes], Awaitable[None]]


class ReportIngestWorker:
    def __init__(self, publish: Publish, gcs: GCSAdapter | None = None):
        self.publish = publish
        self.gcs = gcs or GCSAdapter()

    async def process(self, raw_message: bytes, session: AsyncSession) -> bool:
        payload = json.loads(raw_message)
        report_id = payload.get("report_id")
        if not report_id:
            return False
        report = await session.get(CitizenReport, report_id)
        if report is None:
            return False
        media = [
            {"uri": uri, "bytes_available": bool(self.gcs.download_bytes(uri))}
            for uri in report.media_urls
            if uri.startswith("gs://")
        ]
        await self.publish(
            "climax-ai-dispatch", json.dumps({"report_id": report.id, "media": media}).encode()
        )
        report.status = "TRIAGED"
        await session.commit()
        return True
