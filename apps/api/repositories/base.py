"""
ClimaX Repository Interface Abstraction
Defines the base contract for asynchronous data access layers (SQLAlchemy 2.0 async sessions).
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class IBaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Abstract interface for all domain entity repositories."""

    async def get(self, id: str) -> ModelType | None:
        raise NotImplementedError

    async def list(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        raise NotImplementedError

    async def create(self, schema: CreateSchemaType) -> ModelType:
        raise NotImplementedError

    async def update(self, id: str, schema: UpdateSchemaType) -> ModelType | None:
        raise NotImplementedError

    async def delete(self, id: str) -> bool:
        raise NotImplementedError


class BaseRepository(IBaseRepository[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Reusable SQLAlchemy implementation for simple entity CRUD operations."""

    def __init__(self, session: AsyncSession, model: type[ModelType]):
        self.session = session
        self.model = model

    async def get(self, id: str) -> ModelType | None:
        return await self.session.get(self.model, id)

    async def get_by_id(self, id: str) -> ModelType | None:
        return await self.get(id)

    async def list(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        statement = select(self.model).offset(skip).limit(limit)
        return list((await self.session.scalars(statement)).all())

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        return await self.list(skip, limit)

    async def create(self, schema: CreateSchemaType | dict[str, Any]) -> ModelType:
        data = schema.model_dump(exclude_unset=True) if isinstance(schema, BaseModel) else schema
        entity = self.model(**data)
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def update(self, id: str, schema: UpdateSchemaType | dict[str, Any]) -> ModelType | None:
        entity = await self.get(id)
        if entity is None:
            return None
        data = schema.model_dump(exclude_unset=True) if isinstance(schema, BaseModel) else schema
        for field, value in data.items():
            setattr(entity, field, value)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def delete(self, id: str) -> bool:
        entity = await self.get(id)
        if entity is None:
            return False
        await self.session.delete(entity)
        await self.session.flush()
        return True
