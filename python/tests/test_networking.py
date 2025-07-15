# TODO(airopi): this is outdate code but contains useful fixture that could be reused.

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from wirecraft_server import network

db = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(db)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def local_database(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(network, "async_session", async_session)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
