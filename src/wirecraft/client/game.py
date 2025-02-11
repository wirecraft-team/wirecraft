from __future__ import annotations

import sys
from enum import Enum
from typing import Literal

import pygame

from wirecraft.shared_context import server_var

from .constants import BLACK, FLAGS, FPS, GREY, PADDING, RED, RES_LIST, WHITE
from .server_interface import ServerInterface
from .ui import Button, Cable, Camera, Device, Resolution, Window
from .ui.assets import INVENTORY_BUTTON


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
    def __init__(self, view: Gamestate, resolution: Resolution) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.server = ServerInterface(self)
        self.resolution = resolution
        self.displaysurf = pygame.display.set_mode(self.resolution.size, FLAGS)
        self.camera = Camera(self)
        # Example: get the money
        self.server.get_money()
        self.view = view
        self.click_pos = (6, 9)
        self.devices: list[Device] = []
        self.windows: list[Window] = []
        self.buttons: list[Button] = []
        self.cables: list[Cable] = []
        self.is_placing_cable = False
        pygame.display.set_caption("Wirecraft")

        # Initialize devices  # TODO: remove (debug)
        self.devices.append(Device(self, (0, 0), "switch"))
        # self.devices.append(Device(self, (-200, -200), "switch"))

        # Initialize inventory button
        self.buttons.append(
            Button(
                (0 + PADDING, self.resolution.height - 100 - PADDING),
                (100, 100),
                self.show_inventory,
                INVENTORY_BUTTON,
            )
        )

        self.debug_text = ""

        # For camera panning
        self.dragging = False
        self.last_mouse_pos: tuple[int, int] | None = None

        # For menu interaction
        self.click_handled = False

        self.update_zoom()

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
            server_var.get().stop()
            raise SystemExit(0)

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
        self.windows.append(Window(window_pos, window_size, "Device properties", "Switch"))

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
        """Handle input events."""
        match event.type:
            case pygame.QUIT:
                self.quit_game()
            case pygame.KEYDOWN:
                self.handle_keydown(event)
            case pygame.MOUSEBUTTONDOWN:
                self.handle_mousebuttondown(event, camera)
            case pygame.MOUSEBUTTONUP:
                self.handle_mousebuttonup(event, camera)
            case pygame.MOUSEMOTION:
                self.handle_mousemotion(event, camera)
            case _:
                pass

    def quit_game(self) -> None:
        """Quit the game."""
        server_var.get().stop()
        pygame.quit()
        sys.exit()

    def handle_keydown(self, event: pygame.event.Event) -> None:
        """Handle keydown events."""
        if event.key == pygame.K_ESCAPE:
            if not self.is_placing_cable:
                self.view = Gamestate.MENU
            else:
                self.is_placing_cable = False
                if self.cables:
                    self.cables.pop()

    def handle_mousebuttondown(self, event: pygame.event.Event, camera: Camera) -> None:
        """Handle mouse button down events."""
        match event.button:
            case MouseButtons.WHEEL_UP.value:
                self.adjust_zoom("in")
            case MouseButtons.WHEEL_DOWN.value:
                self.adjust_zoom("out")
            case MouseButtons.LEFT.value:
                self.handle_left_click(camera)
            case MouseButtons.RIGHT.value:
                self.handle_right_click()
            case _:
                pass

    def handle_mousebuttonup(self, event: pygame.event.Event, camera: Camera) -> None:
        """Handle mouse button up events."""

        if event.button == MouseButtons.LEFT.value:
            self.dragging = False
            # if self.click_pos == pygame.mouse.get_pos():
            # button released on the same position as it was clicked
            # if not self.is_placing_cable:
            # self.start_cable_connection(camera)
            # else:
            # self.end_cable_connection(camera)
            self.last_mouse_pos = None
            self.click_handled = False
            self.handle_window_close()
            self.handle_button_click()

    def adjust_zoom(self, amount: Literal["in", "out"]) -> None:
        """Adjust the camera zoom."""
        strategy = self.camera.zoom_out if amount == "out" else self.camera.zoom_in
        changed = strategy(pygame.mouse.get_pos(), self.resolution.size)
        if changed:
            self.update_zoom()

    def set_zoom(self, zoom_value: int):
        changed = self.camera.set_zoom(zoom_value, (0, 0), self.resolution.size)
        if changed:
            self.update_zoom()

    def update_zoom(self):
        # for device in self.devices:
        # device.update_zoom(self.camera)
        for cable in self.cables:
            cable.update_zoom(self.camera)

    def handle_left_click(self, camera: Camera) -> None:
        """Handle left mouse button click."""
        self.click_pos = pygame.mouse.get_pos()
        self.dragging = True
        self.last_mouse_pos = pygame.mouse.get_pos()
        for device in self.devices:
            device.update_position(camera, self.resolution.size)

    # def start_cable_connection(self, camera: Camera) -> None:
    #     """Start a cable connection."""
    #     for device in self.devices:
    #         if device.get_rect().collidepoint(pygame.mouse.get_pos()):
    #             self.cables.append(
    #                 Cable(
    #                     camera.world_to_screen(device.centered_world_position, self.resolution.size),
    #                     pygame.mouse.get_pos(),
    #                 )
    #             )
    #             self.is_placing_cable = True
    #             break

    # def end_cable_connection(self, camera: Camera) -> None:
    #     """End a cable connection."""
    #     for device in self.devices:
    #         if (
    #             device.rect.collidepoint(pygame.mouse.get_pos())
    #             and camera.world_to_screen(device.world_pos, self.resolution.size) != self.cables[-1].start
    #         ):
    #             self.is_placing_cable = False
    #             self.cables[-1].ended = True
    #             self.cables[-1].end = camera.world_to_screen(device.world_pos, self.resolution.size)
    #             break
    #     else:
    #         self.is_placing_cable = False
    #         self.cables[-1].ended = False
    #         self.cables[-1].end = (0, 0)
    #         self.cables.pop()

    def handle_right_click(self) -> None:
        """Handle right mouse button click."""
        for device in self.devices:
            if device.screen_rect.collidepoint(pygame.mouse.get_pos()):
                self.add_device_window(device)

    def handle_window_close(self) -> None:
        """Handle window close button click."""
        for window in self.windows:
            if (
                window.position[0] + window.size[0] - 40
                < pygame.mouse.get_pos()[0]
                < window.position[0] + window.size[0] - 15
                and window.position[1] + 10 < pygame.mouse.get_pos()[1] < window.position[1] + 35
            ):
                self.windows.remove(window)

    def handle_button_click(self) -> None:
        """Handle button click."""
        for button in self.buttons:
            if (
                button.position[0] < pygame.mouse.get_pos()[0] < button.position[0] + button.size[0]
                and button.position[1] < pygame.mouse.get_pos()[1] < button.position[1] + button.size[1]
            ):
                button.action()

    def handle_mousemotion(self, event: pygame.event.Event, camera: Camera) -> None:
        """Handle mouse motion events."""
        if self.dragging and self.view == Gamestate.GAME:
            current_pos = pygame.mouse.get_pos()

            if self.last_mouse_pos:
                dx = int((current_pos[0] - self.last_mouse_pos[0]) / camera.zoom)
                dy = int((current_pos[1] - self.last_mouse_pos[1]) / camera.zoom)
                self.debug_text = f"{self.devices=}"

                for device in self.devices:  # si on clique sur un device, on ne bouge pas la camera
                    if device.screen_rect.collidepoint(current_pos):
                        (x, y) = device.position
                        device.position = (x + dx, y + dy)
                        # self.debug_text = "oue la cest la device"
                        break
                else:
                    camera.x -= dx
                    camera.y -= dy
                    # self.debug_text = "oue la cest la cam"

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

        rect = pygame.Rect(0, 0, 10, 10)
        rect.center = self.camera.world_to_screen((0, 0), self.resolution.size)

        pygame.draw.rect(
            self.displaysurf,
            RED,
            rect,
        )

    def updateview(self) -> None:
        match self.view:
            case Gamestate.GAME:
                self.game()
            case Gamestate.MENU:
                self.menu()
            case Gamestate.SETTINGS:
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
