from repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

from models.entities import Alert


class AlertRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Alert)
