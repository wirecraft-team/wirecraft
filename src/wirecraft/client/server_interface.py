from wirecraft.server import Server


class ServerInterface:
    """
    Ceci est une interface faisant le lien entre le serveur et le client.
    Elle fait partie de la partie "client".
    Elle interagit avec le serveur comme s'il s'agissait d'une librairie, mais pourra être réimplémenté pour se
    connecter à un serveur distant.

    Dans l'état, elle n'est qu'une "duplication" de la partie "server._private", mais permettra une transition simple
    vers un serveur distant sans trop de refactoring.
    """

    def __init__(self) -> None:
        self.connection = Server()

    def get_money(self) -> int:
        return self.connection.get_money()
