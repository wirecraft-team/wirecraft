import sys
from dataclasses import dataclass

import pygame
from pygame.locals import QUIT

from .server_interface import ServerInterface

FPS = pygame.time.Clock()
FPS.tick(30)
BLACK = (0, 0, 0)
RES_LIST = [(3024, 1964), (1920, 1080), (1900, 1200), (1280, 720), (800, 600)]
FLAGS = pygame.FULLSCREEN | pygame.NOFRAME | pygame.SCALED


@dataclass
class Camera:
    x: int
    y: int
    zoom: float


@dataclass
class Resolution:
    width: int
    height: int


class Game:
    def __init__(self, view: str, camera: Camera, resolution: Resolution) -> None:
        pygame.init()
        self.server = ServerInterface()
        self.resolution = resolution
        self.displaysurf = pygame.display.set_mode((self.resolution.width, self.resolution.height), FLAGS)
        self.camera = camera
        # Example: get the money
        self.server.get_money()
        self.view = view
        pygame.display.set_caption("Wirecraft")

    def settings(self) -> None:
        self.view = "settings"
        self.displaysurf.fill((255, 255, 255))
        titlefont = pygame.font.Font(None, 150)
        buttonfont = pygame.font.Font(None, 100)
        title = titlefont.render("Settings", True, BLACK)
        title_rect = title.get_rect(center=(self.resolution.width / 2, self.resolution.height / 5))
        self.displaysurf.blit(title, title_rect)
        for res in RES_LIST:
            res_text = f"{res[0]}x{res[1]}"
            res_render = buttonfont.render(res_text, True, BLACK)
            res_rect = res_render.get_rect(
                center=(self.resolution.width / 2, self.resolution.height / 3 + RES_LIST.index(res) * 100)
            )
            self.displaysurf.blit(res_render, res_rect)
            if res_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.resolution = Resolution(res[0], res[1])
                self.displaysurf = pygame.display.set_mode((self.resolution.width, self.resolution.height), FLAGS)
                with open("settings.json", "w") as file:
                    file.write(
                        f'{{"resolution": {{"width": {self.resolution.width}, "height": {self.resolution.height}}}}}'
                    )
        back = buttonfont.render("Back", True, BLACK)
        back_rect = back.get_rect(center=(self.resolution.width / 2, self.resolution.height / 1.2))
        self.displaysurf.blit(back, back_rect)
        if back_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.menu()

    def menu(self) -> None:
        self.view = "menu"
        self.displaysurf.fill((255, 255, 255))
        titlefont = pygame.font.Font(None, 150)
        buttonfont = pygame.font.Font(None, 100)
        title = titlefont.render("Wirecraft", True, BLACK)
        title_rect = title.get_rect(center=(self.resolution.width / 2, self.resolution.height / 5))
        self.displaysurf.blit(title, title_rect)
        play = buttonfont.render("Play", True, BLACK)
        play_rect = play.get_rect(center=(self.resolution.width / 2, self.resolution.height / 3))
        self.displaysurf.blit(play, play_rect)
        if play_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.game()
        settings = buttonfont.render("Settings", True, BLACK)
        settings_rect = settings.get_rect(center=(self.resolution.width / 2, self.resolution.height / 2))
        self.displaysurf.blit(settings, settings_rect)
        if settings_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.settings()
        exit = buttonfont.render("Exit", True, BLACK)
        exit_rect = exit.get_rect(center=(self.resolution.width / 2, self.resolution.height / 1.5))
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
        device = Device(
            (self.resolution.width / 2 + self.camera.x, self.resolution.height / 2 + self.camera.y),
            "switch",
            self.camera.zoom,
        )
        device.draw(self.displaysurf)
        device1 = Device(
            (self.resolution.width / 3 + self.camera.x, self.resolution.height / 3 + self.camera.y),
            "switch",
            self.camera.zoom,
        )
        device1.draw(self.displaysurf)

    def updateview(self) -> None:
        if self.view == "menu":
            self.menu()
        elif self.view == "game":
            self.updatecam()
            self.game()
        elif self.view == "settings":
            self.settings()

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
        self.image = pygame.image.load(f"assets/{device_type}.png")
        self.image = pygame.transform.scale(
            self.image, (int(self.image.get_width() * zoom), int(self.image.get_height() * zoom))
        )
        self.rect = self.image.get_rect()
        self.rect.center = int(pos[0]), int(pos[1])

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
