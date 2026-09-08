"""
ClimaX Repository Interface Abstraction
Defines the base contract for asynchronous data access layers (SQLAlchemy 2.0 async sessions).
"""

from typing import Generic, TypeVar, Optional, List, Type
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class IBaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Abstract interface for all domain entity repositories."""

    async def get(self, id: str) -> Optional[ModelType]:
        raise NotImplementedError

    async def list(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        raise NotImplementedError

    async def create(self, schema: CreateSchemaType) -> ModelType:
        raise NotImplementedError

    async def update(self, id: str, schema: UpdateSchemaType) -> Optional[ModelType]:
        raise NotImplementedError

    async def delete(self, id: str) -> bool:
        raise NotImplementedError
