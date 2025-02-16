import ctypes
import json
import platform

import click

from wirecraft._logger import init_logger
from wirecraft.client.game import Game, Gamestate
from wirecraft.client.ui import Resolution
from wirecraft.server import Server
from wirecraft.shared_context import ctx, server_var


def init_game():
    iswin = platform.system() == "Windows"
    if iswin:
        ctypes.windll.user32.SetProcessDPIAware()  # type: ignore
    try:
        with open("settings.json") as file:
            settings = json.load(file)
            if not settings["resolution"]["width"] or not settings["resolution"]["height"]:
                settings["resolution"]["width"] = 1920
                settings["resolution"]["height"] = 1080
            resolution = Resolution(settings["resolution"]["width"], settings["resolution"]["height"])
    except FileNotFoundError:
        resolution = Resolution(1920, 1080)

    game = Game(Gamestate.MENU, resolution)
    return game


def init_server():
    server = Server()
    return server


@click.command()
@click.option(
    "--debug", "-d", "debug_options", multiple=True, default=[], envvar="DEBUG", help="Enable debug mode options."
)
def main(debug_options: list[str]):
    ctx.set(debug_options=debug_options)
    init_logger()

    server = init_server()
    server.start()
    server_var.set(server)

    game = init_game()
    game.start()


if __name__ == "__main__":
    main()
