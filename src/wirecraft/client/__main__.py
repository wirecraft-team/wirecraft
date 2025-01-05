import ctypes
import json
import platform

from wirecraft.client import Camera, Game, Resolution


def main():
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
    game = Game("menu", Camera(0, 0, 1), resolution)
    game.start()


if __name__ == "__main__":
    main()
