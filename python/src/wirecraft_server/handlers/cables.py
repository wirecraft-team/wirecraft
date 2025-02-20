from __future__ import annotations

from collections.abc import Sequence

from pydantic import BaseModel
from sqlmodel import select

from ..database.models import Cable, async_session
from ..handlers_core import Handler, event


class PingData(BaseModel):
    content: str


class GetLevelCablesData(BaseModel):
    level_id: int


class CablesHandler(Handler):
    @event
    async def ping(self, data: PingData):
        print(self)
        print(data)
        print(data.content)
        print("pinged")

    @event
    async def get_level_cables(self, data: GetLevelCablesData) -> Sequence[Cable]:
        statement = select(Cable).where(Cable.id_level == data.level_id)
        async with async_session() as session:
            result = await session.exec(statement)
            cables = result.all()
        return cables
