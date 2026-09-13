from uuid import uuid4

from repositories.reports import ReportRepository

from models.entities import CitizenReport
from schemas.entities import CitizenReportCreate


class ReportService:
    def __init__(self, repository: ReportRepository):
        self.repository = repository

    async def submit(self, payload: CitizenReportCreate, user_id: str) -> CitizenReport:
        location = payload.location
        return await self.repository.create(
            {
                "id": str(uuid4()),
                "user_id": user_id,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "geom": f"SRID=4326;POINT({location.longitude} {location.latitude})",
                "address_text": payload.address_text,
                "category": payload.category.value,
                "description": payload.description,
                "media_urls": payload.media_urls,
            }
        )

    async def update_status(self, report_id: str, status: str) -> CitizenReport | None:
        if status not in {"SUBMITTED", "TRIAGED", "LINKED", "CLOSED"}:
            raise ValueError("Invalid report status")
        return await self.repository.update(report_id, {"status": status})
