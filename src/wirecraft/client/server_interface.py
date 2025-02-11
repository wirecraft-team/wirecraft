from __future__ import annotations

from typing import TYPE_CHECKING

from wirecraft.shared_context import server_var

if TYPE_CHECKING:
    from .game import Game


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

        server = server_var.get()
        self.connection = server.new_connection(self)

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

    def get_level_devices(self, level_id: int):
        return self.connection.get_level_devices(level_id)

    def get_level_cables(self, level_id: int):
        return self.connection.get_level_cables(level_id)

    def get_device_pos(self, device_id: int):
        return self.connection.get_device_pos(device_id)

    def get_port_pos(self, port_id: int, device_id: int):
        return self.connection.get_port_pos(port_id, device_id)

    def add_cable(self, id_device_1: int, port_1: int, id_device_2: int, port_2: int, level: int):
        return self.connection.add_cable(id_device_1, port_1, id_device_2, port_2, level)

    def end_cable(self, db_id: int, device_id: int, port_id: int):
        return self.connection.end_cable(db_id, device_id, port_id)

    def delete_cable(self, db_id: int):
        return self.connection.delete_cable(db_id)
