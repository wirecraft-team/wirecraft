import sys
from dataclasses import dataclass
from enum import Enum

import pygame
from pygame.locals import QUIT

from .assets import CLOSE_BUTTON, SWITCH_DEVICE
from .server_interface import ServerInterface

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RES_LIST = [(3024, 1964), (1920, 1080), (1900, 1200)]
FLAGS = pygame.FULLSCREEN | pygame.NOFRAME | pygame.SCALED
FPS = 30


class Gamestate(Enum):
    MENU = 0
    GAME = 1
    SETTINGS = 2


class MouseButtons(Enum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    WHEEL_UP = 4
    WHEEL_DOWN = 5


@dataclass
class Camera:
    x: float
    y: float
    zoom: float
    min_zoom: float = 0.3
    max_zoom: float = 3.0

    def screen_to_world(self, screen_pos: tuple[float, float], screen_size: tuple[int, int]) -> tuple[float, float]:
        """Convert screen coordinates to world coordinates
        screen coordinates are relative to the top left corner of the screen, world coordinates are relative to the center of the screen

        Args:
            screen_pos: the position on the screen
            screen_size: the size of the screen

        Returns:
            the position in the world
        """
        screen_center = (screen_size[0] / 2, screen_size[1] / 2)
        rel_x = (screen_pos[0] - screen_center[0]) / self.zoom
        rel_y = (screen_pos[1] - screen_center[1]) / self.zoom
        return (rel_x + self.x, rel_y + self.y)

    def world_to_screen(self, world_pos: tuple[float, float], screen_size: tuple[int, int]) -> tuple[float, float]:
        """Convert world coordinates to screen coordinates
        screen coordinates are relative to the top left corner of the screen, world coordinates are relative to the center of the screen

        Args:
            world_pos: the position in the world
            screen_size: the size of the screen

        Returns:
            the position on the screen
        """
        screen_center = (screen_size[0] / 2, screen_size[1] / 2)
        rel_x = (world_pos[0] - self.x) * self.zoom
        rel_y = (world_pos[1] - self.y) * self.zoom
        return (screen_center[0] + rel_x, screen_center[1] + rel_y)

    def adjust_zoom(self, delta: float, mouse_pos: tuple[int, int], screen_size: tuple[int, int]):
        """
        Adjust zoom level while maintaining the world position under the mouse cursor.

        Args:
            delta: The amount to change zoom by. Positive values zoom in,
                negative values zoom out.
            mouse_pos: The current mouse position in screen coordinates.
            screen_size: The (width, height) of the screen in pixels.

        Note:
            - Camera position is adjusted to maintain the mouse position
        """
        old_world_pos = self.screen_to_world(mouse_pos, screen_size)
        old_zoom = self.zoom
        self.zoom = max(self.min_zoom, min(self.max_zoom, self.zoom + delta))
        if old_zoom == self.zoom:
            return
        new_screen_pos = self.world_to_screen(old_world_pos, screen_size)
        self.x -= (mouse_pos[0] - new_screen_pos[0]) / self.zoom
        self.y -= (mouse_pos[1] - new_screen_pos[1]) / self.zoom


@dataclass
class Resolution:
    width: int
    height: int

    @property
    def size(self) -> tuple[int, int]:
        return (self.width, self.height)


class Device(pygame.sprite.Sprite):
    def __init__(self, world_pos: tuple[float, float], device_type: str):
        super().__init__()
        self.world_pos = world_pos
        self.base_image = SWITCH_DEVICE
        self.image = self.base_image
        self.rect = self.image.get_rect()

    def update(self, camera: Camera, screen_size: tuple[int, int]):
        """Update device position and scale based on camera"""
        scaled_width = int(self.base_image.get_width() * camera.zoom)
        scaled_height = int(self.base_image.get_height() * camera.zoom)
        self.image = pygame.transform.scale(self.base_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()
        screen_pos = camera.world_to_screen(self.world_pos, screen_size)
        self.rect.center = (int(screen_pos[0]), int(screen_pos[1]))

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)


class Window:
    def __init__(self, position: tuple[float, float], size: tuple[float, float], title: str, data: str) -> None:
        self.position = position
        self.size = size
        self.title = title
        self.data = data

    def draw(self, surface: pygame.Surface) -> None:
        window = pygame.Surface(self.size)
        window.fill(GREY)
        close_button = pygame.transform.scale(CLOSE_BUTTON, (25, 25))
        pygame.draw.rect(window, BLACK, (0, 0, self.size[0], self.size[1]), 5)
        surface.blit(window, self.position)
        surface.blit(close_button, (self.position[0] + self.size[0] - 40, self.position[1] + 10))
        title = pygame.font.Font(None, 50).render(self.title, True, BLACK)
        surface.blit(title, (self.position[0] + 10, self.position[1] + 10))
        text = pygame.font.Font(None, 50).render(self.data, True, BLACK)
        surface.blit(text, (self.position[0] + 10, self.position[1] + 50))


class Game:
    def __init__(self, view: Gamestate, camera: Camera, resolution: Resolution) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.server = ServerInterface()
        self.resolution = resolution
        self.displaysurf = pygame.display.set_mode(self.resolution.size, FLAGS)
        self.camera = camera
        # Example: get the money
        self.server.get_money()
        self.view = view
        self.devices: list[Device] = []
        self.windows: list[Window] = []
        pygame.display.set_caption("Wirecraft")

        # Initialize devices
        self.devices.append(Device((0, 0), "switch"))
        self.devices.append(Device((-200, -200), "switch"))

        # For camera panning
        self.dragging = False
        self.last_mouse_pos: tuple[int, int] | None = None

        # For menu interaction
        self.click_handled = False

    def settings(self) -> None:
        self.view = Gamestate.SETTINGS
        self.displaysurf.fill(WHITE)
        titlefont = pygame.font.Font(None, 150)
        buttonfont = pygame.font.Font(None, 100)

        # Render title
        title = titlefont.render("Settings", True, BLACK)
        title_rect = title.get_rect(center=(self.resolution.width / 2, self.resolution.height / 5))
        self.displaysurf.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0] and not self.click_handled

        for i, res in enumerate(RES_LIST):
            res_text = f"{res[0]}x{res[1]}"
            res_render = buttonfont.render(res_text, True, BLACK)
            res_rect = res_render.get_rect(center=(self.resolution.width / 2, self.resolution.height / 3 + i * 100))
            self.displaysurf.blit(res_render, res_rect)

            if res_rect.collidepoint(mouse_pos) and mouse_clicked:
                self.resolution = Resolution(res[0], res[1])
                self.displaysurf = pygame.display.set_mode(self.resolution.size, FLAGS)
                with open("settings.json", "w") as file:
                    file.write(
                        f'{{"resolution": {{"width": {self.resolution.width}, "height": {self.resolution.height}}}}}'
                    )
                self.click_handled = True

        # Render back button
        back = buttonfont.render("Back", True, BLACK)
        back_rect = back.get_rect(center=(self.resolution.width / 2, self.resolution.height / 1.2))
        self.displaysurf.blit(back, back_rect)

        if back_rect.collidepoint(mouse_pos) and mouse_clicked:
            self.view = Gamestate.MENU
            self.click_handled = True

    def menu(self) -> None:
        self.view = Gamestate.MENU
        self.displaysurf.fill(WHITE)
        titlefont = pygame.font.Font(None, 150)
        buttonfont = pygame.font.Font(None, 100)

        # Render title
        title = titlefont.render("Wirecraft", True, BLACK)
        title_rect = title.get_rect(center=(self.resolution.width / 2, self.resolution.height / 5))
        self.displaysurf.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0] and not self.click_handled

        # Render play button
        play = buttonfont.render("Play", True, BLACK)
        play_rect = play.get_rect(center=(self.resolution.width / 2, self.resolution.height / 3))
        self.displaysurf.blit(play, play_rect)
        if play_rect.collidepoint(mouse_pos) and mouse_clicked:
            self.view = Gamestate.GAME
            self.click_handled = True

        # Render settings button
        settings = buttonfont.render("Settings", True, BLACK)
        settings_rect = settings.get_rect(center=(self.resolution.width / 2, self.resolution.height / 2))
        self.displaysurf.blit(settings, settings_rect)
        if settings_rect.collidepoint(mouse_pos) and mouse_clicked:
            self.view = Gamestate.SETTINGS
            self.click_handled = True

        # Render exit button
        exit = buttonfont.render("Exit", True, BLACK)
        exit_rect = exit.get_rect(center=(self.resolution.width / 2, self.resolution.height / 1.5))
        self.displaysurf.blit(exit, exit_rect)
        if exit_rect.collidepoint(mouse_pos) and mouse_clicked:
            pygame.quit()
            sys.exit()

    def add_device_window(self, device: Device) -> None:
        window_size = (self.resolution.width / 5, self.resolution.height / 5)
        # Position new windows with offset from existing ones
        offset = len(self.windows) * self.resolution.width / 9
        window_pos = (self.resolution.width - window_size[0] - 20, 20 + offset)
        self.windows.append(Window(window_pos, window_size, "Device properties", f"Switch {device.world_pos}"))

    def drawmenu(self, device: Device) -> None:
        # display a window on the top right side of the screen with the device's properties
        window_size = (self.resolution.width / 5, self.resolution.height / 5)
        window_coord = (self.resolution.width - window_size[0] - 20, 20)
        window = pygame.Surface(window_size)
        window.fill(GREY)
        pygame.draw.rect(window, BLACK, (0, 0, window_size[0], window_size[1]), 5)
        self.displaysurf.blit(window, window_coord)
        text = pygame.font.Font(None, 50).render("Device properties", True, BLACK)
        self.displaysurf.blit(text, (window_coord[0] + 10, window_coord[1] + 10))

    def handle_input(self, event: pygame.event.Event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.view = Gamestate.MENU
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MouseButtons.WHEEL_UP.value:
                self.camera.adjust_zoom(0.1, pygame.mouse.get_pos(), self.resolution.size)
            elif event.button == MouseButtons.WHEEL_DOWN.value:
                self.camera.adjust_zoom(-0.1, pygame.mouse.get_pos(), self.resolution.size)
            elif event.button == MouseButtons.LEFT.value and self.view == Gamestate.GAME:
                self.dragging = True
                self.last_mouse_pos = pygame.mouse.get_pos()
            if event.button == MouseButtons.RIGHT.value and self.view == Gamestate.GAME and self.devices:
                for device in self.devices:
                    if device.rect.collidepoint(pygame.mouse.get_pos()):
                        self.add_device_window(device)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == MouseButtons.LEFT.value:
                for window in self.windows:
                    if (
                        window.position[0] + window.size[0] - 40
                        < pygame.mouse.get_pos()[0]
                        < window.position[0] + window.size[0] - 15
                        and window.position[1] + 10 < pygame.mouse.get_pos()[1] < window.position[1] + 35
                    ):
                        self.windows.remove(window)
                self.dragging = False
                self.last_mouse_pos = None
                self.click_handled = False
        elif event.type == pygame.MOUSEMOTION and self.dragging and self.view == Gamestate.GAME:
            current_pos = pygame.mouse.get_pos()
            if self.last_mouse_pos:
                dx = (current_pos[0] - self.last_mouse_pos[0]) / self.camera.zoom
                dy = (current_pos[1] - self.last_mouse_pos[1]) / self.camera.zoom
                self.camera.x -= dx
                self.camera.y -= dy
            self.last_mouse_pos = current_pos

    def game(self) -> None:
        self.displaysurf.fill(WHITE)
        for device in self.devices:
            device.update(self.camera, self.resolution.size)
            device.draw(self.displaysurf)
        for window in self.windows:
            window.draw(self.displaysurf)

    def updateview(self) -> None:
        if self.view == Gamestate.MENU:
            self.menu()
        elif self.view == Gamestate.GAME:
            self.game()
        elif self.view == Gamestate.SETTINGS:
            self.settings()

    def start(self):
        while True:
            for event in pygame.event.get():
                self.handle_input(event)

            self.updateview()
            pygame.display.update()
            self.clock.tick(FPS)
