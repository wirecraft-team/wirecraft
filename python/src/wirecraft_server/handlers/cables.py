from __future__ import annotations

from collections.abc import Sequence

from pydantic import BaseModel
from sqlmodel import select

from ..database import Cable, async_session
from ..handlers_core import Handler, event


class GetLevelCablesData(BaseModel):
    """
    Payload for the get_level_cables ws method.
    """

    level_id: int


class CablesHandler(Handler):
    @event
    async def get_level_cables(self, data: GetLevelCablesData) -> Sequence[Cable]:
        statement = select(Cable).where(Cable.level_id == data.level_id)
        async with async_session() as session:
            result = await session.exec(statement)
            cables = result.all()
        return cables

    @event
    async def add_cable(self, data: Cable):
        async with async_session() as session:
            session.add(data)
            await session.commit()
        return data
