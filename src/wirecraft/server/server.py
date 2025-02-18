from __future__ import annotations

import logging
import threading
import time
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from wirecraft.client.server_interface import ServerInterface


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
        self.client_connexions: list[ServerInterface] = []
        self._last_refresh: float = time.perf_counter()

        self._setup_thread()

    def _setup_thread(self):
        logger.debug("Setup the backend in a separated thread...")
        self._thread = threading.Thread(target=self._run)
        self._stop = threading.Event()

    def _wait_next_refresh(self) -> bool:
        delay = 1 / REFRESH_RATE
        _next = self._last_refresh + delay
        _now = time.perf_counter()
        _wait = _next - _now
        if _wait < 0:
            # TODO: implement server slow down (increase delay in case of poor performances)
            logger.warning("Can't keep up ! %ss behind the normal refresh", -round(_wait, 3))
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
        logger.info("Server started!")
        self._thread.start()

    def stop(self):
        self._stop.set()

    def _run(self):
        while not self._stop.is_set():
            if self._wait_next_refresh():
                logger.info("Server stopped!")
                break

    def get_money(self) -> int:
        return 1000

    def buy_item(self, type: str) -> None:
        return
