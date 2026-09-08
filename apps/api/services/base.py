"""
ClimaX Domain Service Abstraction
Boundary for business logic, transaction management, and orchestrating multiple repositories.
"""

from typing import Generic, TypeVar

RepositoryType = TypeVar("RepositoryType")


class BaseService(Generic[RepositoryType]):
    """Base domain service establishing repository dependency injection."""

    def __init__(self, repository: RepositoryType):
        self.repository = repository
