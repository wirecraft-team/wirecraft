from __future__ import annotations

import threading
from time import sleep
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wirecraft.client import ServerInterface


class Server:
    """
    Cette classe est utilisée pour interagir avec la base de donnée, pour effectuer les différents calcules, sauvegarder
    l'état d'une partie...
    Elle est actuellement utilisée en tant que librairie, mais pourra (à terme) être réimplémentée pour fonctionner
    seule en tant que serveur distant.
    """

    def __init__(self, interface: ServerInterface) -> None:
        self.client_connexion = interface
        self._start_thread()

    def _start_thread(self):
        print("Start backend in separate thread...")
        self._thread = threading.Thread(target=self._run)

    def start(self):
        self.stopped = False
        self._thread.start()

    def stop(self):
        self.stopped = True

    def _run(self):
        while self.stopped is False:
            sleep(5)
            print("HERE")
            self.client_connexion.money_update()

    def get_money(self) -> int:
        return 1000

    def buy_item(self, type: str) -> None:
        return
