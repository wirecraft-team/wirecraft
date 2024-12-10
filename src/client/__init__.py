import sys

import pygame
from pygame.locals import QUIT

from server import get_value

FPS = pygame.time.Clock()
FPS.tick(30)
BLACK = (0, 0, 0)


class Game:
    def __init__(self, view: str) -> None:
        pygame.init()
        self.displaysurf = pygame.display.set_mode((1920, 1080))
        self.view = view
        # pygame.display.set_caption(get_value())
        pygame.display.set_caption("Wirecraft")

    def menu(self) -> None:
        self.view = "menu"
        self.displaysurf.fill((255, 255, 255))
        titlefont = pygame.font.Font(None, 150)
        buttonfont = pygame.font.Font(None, 100)
        title = titlefont.render("Wirecraft", True, BLACK)
        title_rect = title.get_rect(center=(1920 / 2, 1080 / 5))
        self.displaysurf.blit(title, title_rect)
        play = buttonfont.render("Play", True, BLACK)
        play_rect = play.get_rect(center=(1920 / 2, 1080 / 2))
        self.displaysurf.blit(play, play_rect)
        if play_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.game()

    def game(self) -> None:
        self.view = "game"
        self.displaysurf.fill((255, 255, 255))
        device = Device((1920 / 2, 1080 / 2), "switch")
        device.draw(self.displaysurf)

    def updateview(self) -> None:
        if self.view == "menu":
            self.menu()
        elif self.view == "game":
            self.game()

    def start(self):
        while True:  # main game loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.view = "menu"
            self.updateview()
            pygame.display.update()


class Device(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, device_type: str):
        super().__init__()
        self.image = pygame.image.load(f"assets/{device_type}.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)
