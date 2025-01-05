class Server:
    """
    Cette classe est utilisée pour interagir avec la base de donnée, pour effectuer les différents calcules, sauvegarder
    l'état d'une partie...
    Elle est actuellement utilisée en tant que librairie, mais pourra (à terme) être réimplémentée pour fonctionner
    seule en tant que serveur distant.
    """

    def get_money(self) -> int:
        return 1000
