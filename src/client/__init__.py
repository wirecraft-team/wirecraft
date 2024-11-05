import sys

import pygame
from pygame.locals import QUIT

from server import get_value


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.displaysurf = pygame.display.set_mode((400, 300))

        pygame.display.set_caption(get_value())

    def start(self):
        while True:  # main game loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
