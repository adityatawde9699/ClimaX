"""Concrete repository bindings for core ClimaX domain entities."""

from repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

from models.entities import (
    Alert,
    CitizenReport,
    EnvironmentalObservation,
    Incident,
    Intervention,
    Organization,
    Sensor,
    User,
)


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)


class OrganizationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Organization)


class SensorRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Sensor)


class ObservationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, EnvironmentalObservation)


class ReportRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, CitizenReport)


class IncidentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Incident)


class AlertRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Alert)


class InterventionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Intervention)
