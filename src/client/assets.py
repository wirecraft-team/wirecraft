from importlib.resources import files

import pygame

try:
    assets_dir = files("wirecraft").joinpath("assets")
except ModuleNotFoundError:  # we are in dev mode
    assets_dir = "./assets"

SWITCH_DEVICE = pygame.image.load(f"{assets_dir}/switch.png")
