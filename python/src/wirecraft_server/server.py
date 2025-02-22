from __future__ import annotations

import asyncio
import contextlib
import logging
import time
from collections.abc import Sequence
from typing import Any, Self

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .database.models import Cable, Device, engine

REFRESH_RATE = 30

logger = logging.getLogger(__name__)


class Server:
    """
    Cette classe est utilisée pour interagir avec la base de donnée, pour effectuer les différents calcules, sauvegarder
    l'état d'une partie...
    Elle est actuellement utilisée en tant que librairie, mais pourra (à terme) être réimplémentée pour fonctionner
    seule en tant que serveur distant.
    """

    def __init__(self) -> None:
        self.client_connexions: list[Any] = []  # TODO(airopi): WS
        self._last_refresh: float = time.perf_counter()

        # nb: if this event is set, the server will stop
        # This is used if we *need* to stop the server in any other way than CTRL+C
        # Or if we have tasks that need to finish properly before stopping, so they know they should stop without having
        # to cancel them.
        self._stop = asyncio.Event()

    def start(self):
        logger.info("Server started!")
        try:
            asyncio.run(self._run())
        except KeyboardInterrupt:
            logger.info("Server stopped!")
            self._stop.set()  # if some tasks depends on this event
        except Exception:
            logger.exception("Server crashed!")
            raise SystemExit(1)

    async def _wait_next_refresh(self):
        delay = 1 / REFRESH_RATE
        _next = self._last_refresh + delay
        _now = time.perf_counter()
        _wait = _next - _now
        if _wait < 0:
            # TODO(airopi): implement server slow down (increase delay in case of poor performances)
            logger.warning("Can't keep up ! %ss behind the normal refresh", -round(_wait, 3))
            self._last_refresh = _now
            return self._stop.is_set()

        self._last_refresh = _next
        with contextlib.suppress(asyncio.TimeoutError):
            await asyncio.wait_for(self._stop.wait(), _wait)
        return self._stop.is_set()

    def new_connection(self, interface: Any) -> Self:  # TODO(airopi): WS
        self.client_connexions.append(interface)
        return self

    def disconnect(self, interface: Any):  # TODO(airopi): WS
        self.client_connexions.remove(interface)

    async def _run(self):
        while True:
            stopped = await self._wait_next_refresh()
            if stopped:
                logger.info("Server stopped!")
                break

    async def add_cable(self, id_device_1: int, port_1: int, id_device_2: int, port_2: int, level: int) -> bool:
        # check if port is available
        async with AsyncSession(engine) as session:
            statement = select(Cable).where(
                Cable.id_device_1 == id_device_1, Cable.port_1 == port_1, Cable.id_level == level
            )
            result = await session.exec(statement)
            if result.first():
                return False
            # Next line is strange to read but trust me, it works
            statement = select(Cable).where(
                Cable.id_device_2 == id_device_1, Cable.port_2 == port_1, Cable.id_level == level
            )
            result = await session.exec(statement)
            if result.first():
                return False
            statement = Cable(
                id_device_1=id_device_1, port_1=port_1, id_device_2=id_device_2, port_2=port_2, id_level=level
            )
            session.add(statement)
            await session.commit()
        return True

    async def end_cable(self, cable_id: int, device_id: int, port_id: int) -> bool:
        # check if port is available
        async with AsyncSession(engine) as session:
            level = select(Device.id_level).where(Device.id == device_id)
            result = await session.exec(level)
            level = result.one()
            statement = select(Cable).where(
                Cable.id_device_2 == device_id, Cable.port_2 == port_id, Cable.id_level == level
            )

            result = await session.exec(statement)
            if result.first():
                return False

            # Again, strange to read but works
            statement = select(Cable).where(
                Cable.id_device_1 == device_id, Cable.port_1 == port_id, Cable.id_level == level
            )
            result = await session.exec(statement)
            if result.first():
                return False

            statement = select(Cable).where(Cable.id == cable_id)
            result = await session.exec(statement)
            cable = result.one()
            cable.id_device_2 = device_id
            cable.port_2 = port_id

            session.add(cable)
            await session.commit()
        return True

    async def get_level_cables(self, id_level: int) -> Sequence[Cable]:
        statement = select(Cable).where(Cable.id_level == id_level)
        async with AsyncSession(engine) as session:
            result = await session.exec(statement)
            return result.all()

    async def get_level_devices(self, id_level: int) -> Sequence[Device]:
        statement = select(Device).where(Device.id_level == id_level)
        async with AsyncSession(engine) as session:
            result = await session.exec(statement)
            return result.all()

    async def get_device_pos(self, device_id: int):
        statement = select(Device.x, Device.y).where(Device.id == device_id)
        async with AsyncSession(engine) as session:
            result = await session.exec(statement)
            return result.one()

    async def delete_cable(self, cable_id: int):
        statement = select(Cable).where(Cable.id == cable_id)
        async with AsyncSession(engine) as session:
            result = await session.exec(statement)
            cable = result.one()

            await session.delete(cable)
            await session.commit()
            logger.debug("Cable deleted")

    async def get_task_list(self, level: int) -> list[str]:
        # Server send task list to client based on level
        return ["This is the first task", "This is the second task", "This is the third task"]
