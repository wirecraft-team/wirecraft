import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from wirecraft_server import network
from wirecraft_server.database.models import Cable, Device, LevelState

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
        device_a = Device(name="Test PC A", type="pc", x=0, y=0, level_id=level_dev.id, ip="192.168.0.2")
        device_b = Device(name="Test PC B", type="pc", x=100, y=100, level_id=level_dev.id, ip="192.168.0.2")
        session.add_all([device_a, device_b])
        await session.flush()

        session.add(
            Cable(
                device_id_1=device_a.id,
                port_1=1,
                device_id_2=device_b.id,
                port_2=1,
                level_id=level_dev.id,
            )
        )
        await session.commit()
    print(device_a.id, device_b.id)

    await network.update_devices()
    await network.update_routing_tables()

    async with async_session() as session:
        # Retrieve the device and test ping
        device = await session.get(Device, 1)
        assert device is not None
