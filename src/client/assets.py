from importlib.resources import files

import pygame

assets_dir = files("wirecraft").joinpath("assets")

SWITCH_DEVICE = pygame.image.load(f"{assets_dir}/switch.png")
