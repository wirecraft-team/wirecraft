import sys
from dataclasses import dataclass

import pygame
from pygame.locals import QUIT

from .assets import SWITCH_DEVICE
from .server_interface import ServerInterface

FPS = pygame.time.Clock()
FPS.tick(30)
BLACK = (0, 0, 0)


@dataclass
class Camera:
    x: int
    y: int
    zoom: float


class Game:
    def __init__(self, view: str, camera: Camera) -> None:
        pygame.init()
        self.server = ServerInterface()
        flags = pygame.FULLSCREEN | pygame.NOFRAME | pygame.SCALED
        self.displaysurf = pygame.display.set_mode((1920, 1080), flags)
        self.camera = camera
        # Example: get the money
        self.server.get_money()
        # self.displaysurf = pygame.display.set_mode((1920, 1080))
        self.view = view
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
        exit = buttonfont.render("Exit", True, BLACK)
        exit_rect = exit.get_rect(center=(1920 / 2, 1080 / 1.5))
        self.displaysurf.blit(exit, exit_rect)
        if exit_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            pygame.quit()
            sys.exit()

    def updatecam(self) -> None:
        # TODO Add support for mouse drag and touchpad two finger drag
        # TODO This is terrible, fix it
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.camera.x -= 5
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.camera.x += 5
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.camera.y -= 5
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.camera.y += 5

    def game(self) -> None:
        self.view = "game"
        self.displaysurf.fill((255, 255, 255))
        device = Device((1920 / 2 + self.camera.x, 1080 / 2 + self.camera.y), "switch", self.camera.zoom)
        device.draw(self.displaysurf)
        device1 = Device((1920 / 3 + self.camera.x, 1080 / 3 + self.camera.y), "switch", self.camera.zoom)
        device1.draw(self.displaysurf)

    def updateview(self) -> None:
        if self.view == "menu":
            self.menu()
        elif self.view == "game":
            self.updatecam()
            self.game()

    def start(self):
        while True:  # main game loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.view = "menu"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.camera.zoom += 0.1
                    if event.button == 5 and self.camera.zoom > 0.3:
                        self.camera.zoom -= 0.1
            self.updateview()
            pygame.display.update()


class Device(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], device_type: str, zoom: float = 1):
        super().__init__()
        self.image = SWITCH_DEVICE
        self.image = pygame.transform.scale(
            self.image, (int(self.image.get_width() * zoom), int(self.image.get_height() * zoom))
        )
        self.rect = self.image.get_rect()
        self.rect.center = int(pos[0]), int(pos[1])

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
