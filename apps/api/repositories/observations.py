from repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

from models.entities import EnvironmentalObservation


class ObservationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, EnvironmentalObservation)
