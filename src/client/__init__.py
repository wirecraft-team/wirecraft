import sys

import pygame
from pygame.locals import QUIT

from .server_interface import ServerInterface


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.server = ServerInterface()
        self.displaysurf = pygame.display.set_mode((400, 300))

        # Example: get the money
        self.server.get_money()

    def start(self):
        while True:  # main game loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
