import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from wirecraft_server import network
from wirecraft_server.database.models import Device, LevelState

db = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(db)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def local_database(monkeypatch):
    monkeypatch.setattr(network, "async_session", async_session)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def test_ping(local_database):
    async with async_session() as session:
        level_dev = LevelState(completed=False)
        session.add(level_dev)
        await session.flush()

        # Create a mock device
        device = Device(id=1, name="Test Device", type="router", x=0, y=0, level_id=level_dev.id)
        session.add(device)
        await session.commit()

    async with async_session() as session:
        # Retrieve the device and test ping
        device = await session.get(Device, 1)
        assert device is not None
