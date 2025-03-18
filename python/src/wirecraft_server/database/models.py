from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import (
    Field,  # type: ignore
    SQLModel,
    select,
)
from sqlmodel.ext.asyncio.session import AsyncSession

db = "sqlite+aiosqlite:///database.db"
engine = create_async_engine(db)


async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Cable(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    device_id_1: int = Field(default=None, foreign_key="device.id")
    port_1: int
    device_id_2: int = Field(default=None, foreign_key="device.id")
    port_2: int
    level_id: int = Field(default=None, foreign_key="level.id")


class Device(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    type: str
    x: int
    y: int
    level_id: int = Field(default=None, foreign_key="level.id")


class Level(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    completed: bool = False


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    level_id: int = Field(default=None, foreign_key="level.id")
    name: str
    completed: bool = False


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    level_dev = Level(completed=False)
    # Add level first to get an ID before assigning it to devices
    async with async_session() as session:
        if not (await session.exec(select(Level))).first():
            session.add(level_dev)
            await session.commit()
            await session.refresh(level_dev)
            if TYPE_CHECKING:
                assert isinstance(level_dev.id, int)
            switch1 = Device(name="sw1", type="switch", x=0, y=0, level_id=level_dev.id)
            pc1 = Device(name="pc1", type="pc", x=400, y=-400, level_id=level_dev.id)
            pc2 = Device(name="pc2", type="pc", x=-400, y=-400, level_id=level_dev.id)
            session.add(switch1)
            session.add(pc1)
            session.add(pc2)
            await session.commit()
            cable = Cable(device_id_1=switch1.id, port_1=1, device_id_2=pc1.id, port_2=1, level_id=level_dev.id)
            session.add(cable)
            await session.commit()
    # if there are cables with devices id that are < 0 then delete them as they were in a placing state when the game closed
    async with async_session() as session:
        cables = (await session.exec(select(Cable))).all()
        for cable in cables:
            if cable.device_id_1 < 0:
                await session.delete(cable)
        await session.commit()
