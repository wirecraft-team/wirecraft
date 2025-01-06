from __future__ import annotations

from typing import TYPE_CHECKING

from wirecraft.server import Server

if TYPE_CHECKING:
    from wirecraft.client import Game


def event[T](f: T) -> T:
    """
    This is a fake function. Just to simulate like if we had a websocket connection etc.

    But, from the Server side, instead of doing something like:
    ```python
    client.send_msg("update_this", data=serialized_data)
    ```
    And having a logic to handle the message and call the correct function from the client side

    We just do
    ```python
    interface.update_this(data)
    ```
    And the server call directly the client.
    """
    return f


class ServerInterface:
    """
    Ceci est une interface faisant le lien entre le serveur et le client.
    Elle fait partie de la partie "client".
    Elle interagit avec le serveur comme s'il s'agissait d'une librairie, mais pourra être réimplémenté pour se
    connecter à un serveur distant.

    Dans l'état, elle n'est qu'une "duplication" de la partie "server._private", mais permettra une transition simple
    vers un serveur distant sans trop de refactoring.
    """

    def __init__(self, game: Game) -> None:
        self.game = game
        self.connection = Server(self)
        self.connection.start()

    def close_connection(self):
        self.connection.stop()

    def get_money(self) -> int:
        # The client can ask for data to the server
        return self.connection.get_money()

    def buy_item(self, type: str) -> None:
        # The client can send data to the server
        return self.connection.buy_item(type)

    @event
    def money_update(self) -> None:
        # the server side can send event to client
        print("money updated")
