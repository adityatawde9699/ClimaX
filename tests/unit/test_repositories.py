from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from repositories.base import BaseRepository

from models.entities import User


@pytest.mark.asyncio
async def test_base_repository_crud_contract():
    result = Mock()
    existing = User(id="one", email="one@example.com", full_name="One", password_hash="hash")
    result.all.return_value = [existing]
    session = SimpleNamespace(
        get=AsyncMock(return_value=existing),
        scalars=AsyncMock(return_value=result),
        add=Mock(),
        flush=AsyncMock(),
        refresh=AsyncMock(),
        delete=AsyncMock(),
    )
    repository = BaseRepository(session, User)
    assert (await repository.get("one")).id == "one"
    assert len(await repository.list()) == 1
    created = await repository.create(
        {"id": "two", "email": "two@example.com", "full_name": "Two", "password_hash": "hash"}
    )
    assert created.id == "two"
    updated = await repository.update("one", {"name": "updated"})
    assert updated.name == "updated"
    assert await repository.delete("one") is True


@pytest.mark.asyncio
async def test_base_repository_missing_entity_contract():
    session = SimpleNamespace(get=AsyncMock(return_value=None))
    repository = BaseRepository(session, User)
    assert await repository.update("missing", {}) is None
    assert await repository.delete("missing") is False
