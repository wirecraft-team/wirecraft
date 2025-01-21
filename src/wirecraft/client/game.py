from __future__ import annotations

import sys
from enum import Enum
from typing import TYPE_CHECKING

import pygame
from pygame.locals import QUIT

from .constants import BLACK, FLAGS, FPS, GREY, PADDING, RES_LIST, WHITE
from .server_interface import ServerInterface
from .ui import Button, Cable, Device, Resolution, Window
from .ui.assets import INVENTORY_BUTTON

if TYPE_CHECKING:
    from .ui import Camera


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


class Game:
    def __init__(self, view: Gamestate, camera: Camera, resolution: Resolution) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.server = ServerInterface(self)
        self.resolution = resolution
        self.displaysurf = pygame.display.set_mode(self.resolution.size, FLAGS)
        self.camera = camera
        # Example: get the money
        self.server.get_money()
        self.view = view
        self.devices: list[Device] = []
        self.windows: list[Window] = []
        self.buttons: list[Button] = []
        self.cables: list[Cable] = []
        self.is_placing_cable = False
        pygame.display.set_caption("Wirecraft")

        # Initialize devices
        self.devices.append(Device((0, 0), "switch"))
        self.devices.append(Device((-200, -200), "switch"))

        # Initialize inventory button
        self.buttons.append(
            Button(
                (0 + PADDING, self.resolution.height - 100 - PADDING),
                (100, 100),
                self.show_inventory,
                INVENTORY_BUTTON,
            )
        )

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

        # Render resolution list
        for i, res in enumerate(RES_LIST):
            res_text = f"{res[0]}x{res[1]}"
            res_render = buttonfont.render(res_text, True, BLACK)
            res_rect = res_render.get_rect(center=(self.resolution.width / 2, self.resolution.height / 3 + i * 100))
            self.displaysurf.blit(res_render, res_rect)

            # Change and save resolution
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
        """Add a window displaying the properties of a device."""
        window_size = (self.resolution.width / 5, self.resolution.height / 5)
        # Position new windows with offset from existing ones
        offset = len(self.windows) * self.resolution.width / 9
        window_pos = (self.resolution.width - window_size[0] - 20, 20 + offset)
        # If we are out of bounds, don't create the window
        if (
            window_pos[0] > self.resolution.width - window_size[0] - 20
            or window_pos[1] > self.resolution.height - window_size[1] - 20
        ):
            return
        self.windows.append(Window(window_pos, window_size, "Device properties", f"Switch {device.world_pos}"))

    def drawmenu(self, device: Device) -> None:
        """display a window on the top right side of the screen with the device's properties"""
        window_size = (self.resolution.width / 5, self.resolution.height / 5)
        window_coord = (self.resolution.width - window_size[0] - 20, 20)
        window = pygame.Surface(window_size)
        window.fill(GREY)
        pygame.draw.rect(window, BLACK, (0, 0, window_size[0], window_size[1]), 5)
        self.displaysurf.blit(window, window_coord)
        text = pygame.font.Font(None, 50).render("Device properties", True, BLACK)
        self.displaysurf.blit(text, (window_coord[0] + 10, window_coord[1] + 10))

    def handle_input(self, event: pygame.event.Event, camera: Camera) -> None:
        """handle input events."""
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.view = Gamestate.MENU
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle zoom
            if event.button == MouseButtons.WHEEL_UP.value:
                self.camera.adjust_zoom(0.1, pygame.mouse.get_pos(), self.resolution.size)
                for device in self.devices:
                    device.update_zoom(self.camera)
                for cable in self.cables:
                    cable.update_zoom(self.camera)
            elif event.button == MouseButtons.WHEEL_DOWN.value:
                self.camera.adjust_zoom(-0.1, pygame.mouse.get_pos(), self.resolution.size)
                for device in self.devices:
                    device.update_zoom(self.camera)
                for cable in self.cables:
                    cable.update_zoom(self.camera)

            # Handle panning
            elif event.button == MouseButtons.LEFT.value and self.view == Gamestate.GAME:
                # if click is on switch device, start a cable connection
                if not self.is_placing_cable:
                    for device in self.devices:
                        if device.rect.collidepoint(pygame.mouse.get_pos()):
                            self.cables.append(
                                Cable(
                                    camera.world_to_screen(device.world_pos, self.resolution.size),
                                    pygame.mouse.get_pos(),
                                )
                            )
                            self.is_placing_cable = True
                            break
                else:
                    for device in self.devices:
                        if (
                            device.rect.collidepoint(pygame.mouse.get_pos())
                            and camera.world_to_screen(device.world_pos, self.resolution.size) != self.cables[-1].start
                        ):
                            self.is_placing_cable = False
                            self.cables[-1].ended = True
                            self.cables[-1].end = camera.world_to_screen(device.world_pos, self.resolution.size)
                            break
                self.dragging = True
                self.last_mouse_pos = pygame.mouse.get_pos()
                for device in self.devices:
                    device.update_position(self.camera, self.resolution.size)

        elif event.type == pygame.MOUSEBUTTONUP:
            # Handle right click on devices
            if event.button == MouseButtons.RIGHT.value and self.view == Gamestate.GAME and self.devices:
                for device in self.devices:
                    if device.rect.collidepoint(pygame.mouse.get_pos()):
                        self.add_device_window(device)

            if event.button == MouseButtons.LEFT.value:
                self.dragging = False
                self.last_mouse_pos = None
                self.click_handled = False
                # Handle close button
                for window in self.windows:
                    if (
                        window.position[0] + window.size[0] - 40
                        < pygame.mouse.get_pos()[0]
                        < window.position[0] + window.size[0] - 15
                        and window.position[1] + 10 < pygame.mouse.get_pos()[1] < window.position[1] + 35
                    ):
                        self.windows.remove(window)
                # Handle click on buttons
                for button in self.buttons:
                    if (
                        button.position[0] < pygame.mouse.get_pos()[0] < button.position[0] + button.size[0]
                        and button.position[1] < pygame.mouse.get_pos()[1] < button.position[1] + button.size[1]
                    ):
                        button.action()

        # Handle panning
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

        # Update and draw devices
        for device in self.devices:
            device.update_position(self.camera, self.resolution.size)
            device.draw(self.displaysurf)

        # Update and draw windows
        for i, window in enumerate(self.windows):
            if window.title != "Inventory":
                window.update_pos(i, self.resolution)
            window.draw(self.displaysurf)

        # Draw buttons
        for button in self.buttons:
            button.draw(self.displaysurf)

        # Draw cables
        for cable in self.cables:
            if not cable.ended:
                cable.end = pygame.mouse.get_pos()
            cable.update_position(self.camera, self.resolution)
            cable.draw(self.displaysurf, self.camera, resolution=self.resolution)

        # add a debug text for self.is_placing_cable
        debug_text = pygame.font.Font(None, 30).render(f"Placing Cable: {self.is_placing_cable}", True, BLACK)
        self.displaysurf.blit(debug_text, (10, 10))

    def updateview(self) -> None:
        if self.view == Gamestate.MENU:
            self.menu()
        elif self.view == Gamestate.GAME:
            self.game()
        elif self.view == Gamestate.SETTINGS:
            self.settings()

    def start(self):
        """main game loop."""
        while True:
            for event in pygame.event.get():
                self.handle_input(event, self.camera)

            self.updateview()
            pygame.display.update()
            self.clock.tick(FPS)

    def show_inventory(self):
        """Inventory button action."""
        # display a window on the right side taking all the height of the screen
        self.windows.append(
            Window(
                (self.resolution.width - self.resolution.width / 5 - 20, 20),
                (self.resolution.width / 5, self.resolution.height - 40),
                "Inventory",
                "You have 10 switches",
            )
        )
