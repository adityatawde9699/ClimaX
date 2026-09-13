from repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

from models.entities import Prediction


class PredictionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Prediction)
