import ctypes
import json
import platform

from wirecraft.client.game import Game, Gamestate
from wirecraft.client.ui import Camera, Resolution
from wirecraft.server import Server
from wirecraft.shared_context import server_var


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

    game = Game(Gamestate.MENU, Camera(0, 0, 1), resolution)
    return game


def init_server():
    server = Server()
    return server


def main():
    server = init_server()
    server.start()
    server_var.set(server)

    game = init_game()
    game.start()


if __name__ == "__main__":
    main()
