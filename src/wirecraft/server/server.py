from __future__ import annotations

import threading
import time
from collections.abc import Sequence
from typing import TYPE_CHECKING, Self

from sqlmodel import Session, select

from .database.models import Cable, Device, engine

if TYPE_CHECKING:
    from wirecraft.client.server_interface import ServerInterface


REFRESH_RATE = 30
# TODO: implement error checking


class Server:
    """
    Cette classe est utilisée pour interagir avec la base de donnée, pour effectuer les différents calcules, sauvegarder
    l'état d'une partie...
    Elle est actuellement utilisée en tant que librairie, mais pourra (à terme) être réimplémentée pour fonctionner
    seule en tant que serveur distant.
    """

    def __init__(self) -> None:
        self.client_connexions: list[ServerInterface] = []
        self._last_refresh: float = time.perf_counter()

        self._setup_thread()

    def _setup_thread(self):
        print("Setup the backend in a separated thread...")
        self._thread = threading.Thread(target=self._run)
        self._stop = threading.Event()

    def _wait_next_refresh(self) -> bool:
        delay = 1 / REFRESH_RATE
        _next = self._last_refresh + delay
        _now = time.perf_counter()
        _wait = _next - _now
        if _wait < 0:
            # TODO: implement server slow down (increase delay in case of poor performances)
            print(f"WARNING: can't keep up ! {_wait}s behind the normal refresh")
            self._last_refresh = _now
            return self._stop.is_set()

        self._last_refresh = _next
        return self._stop.wait(_wait)

    def new_connection(self, interface: ServerInterface) -> Self:
        self.client_connexions.append(interface)
        return self

    def disconnect(self, interface: ServerInterface):
        self.client_connexions.remove(interface)

    def start(self):
        print("Server started!")
        self._thread.start()

    def stop(self):
        self._stop.set()

    def _run(self):
        while not self._stop.is_set():
            if self._wait_next_refresh():
                print("Server stopped!")
                break

    def get_money(self) -> int:
        return 1000

    def buy_item(self, type: str) -> None:
        return

    def add_cable(self, id_device_1: int, port_1: int, id_device_2: int, port_2: int, level: int) -> bool:
        # check if port is available
        with Session(engine) as session:
            statement = select(Cable).where(
                Cable.id_device_1 == id_device_1, Cable.port_1 == port_1, Cable.id_level == level
            )
            if session.exec(statement).first():
                return False
            # Next line is strange to read but trust me, it works
            statement = select(Cable).where(
                Cable.id_device_2 == id_device_1, Cable.port_2 == port_1, Cable.id_level == level
            )
            if session.exec(statement).first():
                return False
            statement = Cable(
                id_device_1=id_device_1, port_1=port_1, id_device_2=id_device_2, port_2=port_2, id_level=level
            )
            session.add(statement)
            session.commit()
        return True

    def end_cable(self, cable_id: int, device_id: int, port_id: int) -> bool:
        # check if port is available
        with Session(engine) as session:
            level = select(Device.id_level).where(Device.id == device_id)
            level = session.exec(level).one()
            statement = select(Cable).where(
                Cable.id_device_2 == device_id, Cable.port_2 == port_id, Cable.id_level == level
            )
            if session.exec(statement).first():
                return False
            # Again, strange to read but works
            statement = select(Cable).where(
                Cable.id_device_1 == device_id, Cable.port_1 == port_id, Cable.id_level == level
            )
            if session.exec(statement).first():
                return False
            statement = select(Cable).where(Cable.id == cable_id)
            cable = session.exec(statement).one()
            cable.id_device_2 = device_id
            cable.port_2 = port_id
            session.add(cable)
            session.commit()
        return True

    def get_level_cables(self, id_level: int) -> Sequence[Cable]:
        statement = select(Cable).where(Cable.id_level == id_level)
        with Session(engine) as session:
            return session.exec(statement).all()

    def get_level_devices(self, id_level: int) -> Sequence[Device]:
        statement = select(Device).where(Device.id_level == id_level)
        with Session(engine) as session:
            return session.exec(statement).all()

    def get_device_pos(self, device_id: int):
        statement = select(Device.x, Device.y).where(Device.id == device_id)
        with Session(engine) as session:
            return session.exec(statement).one()

    def get_port_pos(self, port_id: int, device_id: int):
        # TODO: implement port position
        return (100, 24)

    def delete_cable(self, cable_id: int):
        statement = select(Cable).where(Cable.id == cable_id)
        with Session(engine) as session:
            cable = session.exec(statement).one()
            session.delete(cable)
            session.commit()
            print("Cable deleted")

    def get_task_list(self, level: int) -> list[str]:
        # Server send task list to client based on level
        return ["This is the first task", "This is the second task", "This is the third task"]
