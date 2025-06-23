from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel

from .models import Cable as Cable, Device as Device, LevelState as LevelState
from .session import async_session as async_session


async def init_db(engine: AsyncEngine):
    """
    TODO(airopi): stop destroying the database on every start.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
