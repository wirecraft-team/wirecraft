import os
from importlib.resources import files

import pygame

# Check for assets in the package if installed
assets_dir = str(files("wirecraft").joinpath("assets"))

# Otherwise check on the local directory if executed in dev environnement
if not os.path.exists(assets_dir):
    assets_dir = "./assets"

SWITCH_DEVICE = pygame.image.load(f"{assets_dir}/switch.png")

PC_DEVICE = pygame.image.load(f"{assets_dir}/pc.png")
