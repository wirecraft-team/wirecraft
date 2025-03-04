from __future__ import annotations

from collections.abc import Sequence

from pydantic import BaseModel
from sqlmodel import select

from ..database.models import Cable, async_session
from ..handlers_core import Handler, event


class GetLevelCablesData(BaseModel):
    level_id: int


class AddCableData(BaseModel):
    id_device_1: int
    port_1: int
    id_device_2: int
    port_2: int
    id_level: int


class CablesHandler(Handler):
    @event
    async def ping(self):
        print("pinged")
        return "pong"

    @event
    async def get_level_cables(self, data: GetLevelCablesData) -> Sequence[Cable]:
        statement = select(Cable).where(Cable.id_level == data.level_id)
        async with async_session() as session:
            result = await session.exec(statement)
            cables = result.all()
        return cables

    @event
    async def add_cable(self, data: Cable):
        async with async_session() as session:
            session.add(data)
            await session.commit()
