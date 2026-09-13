from uuid import uuid4

from fastapi import HTTPException
from repositories.users import UserRepository
from security.jwt import hash_password
from sqlalchemy import select

from models.entities import User
from schemas.entities import UserCreate, UserRole, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create(self, payload: UserCreate) -> User:
        if await self.repository.session.scalar(select(User).where(User.email == payload.email)):
            raise HTTPException(409, "Email is already registered")
        data = payload.model_dump(exclude={"password"})
        data["role"] = payload.role.value
        return await self.repository.create(
            {"id": str(uuid4()), "password_hash": hash_password(payload.password), **data}
        )

    async def update(self, user_id: str, payload: UserUpdate) -> User | None:
        data = payload.model_dump(exclude_unset=True)
        if isinstance(data.get("role"), UserRole):
            data["role"] = data["role"].value
        return await self.repository.update(user_id, data)
