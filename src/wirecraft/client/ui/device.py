from __future__ import annotations

import time
from typing import TYPE_CHECKING, cast

import pygame

from .assets import SWITCH_DEVICE
from .camera import WorldObjectBounds

if TYPE_CHECKING:
    from ..game import Game
    from .camera import Camera


class Device(pygame.sprite.Sprite):
    def __init__(self, game: Game, position: tuple[int, int], device_type: str):
        """
        Position is the point in the world map that refer to the center of the device.
        """
        super().__init__()
        self.game = game
        self.position: tuple[int, int] = position
        self.base_image = SWITCH_DEVICE.convert_alpha()
        self.size = (SWITCH_DEVICE.get_width(), SWITCH_DEVICE.get_height())

    def get_rect(self) -> pygame.Rect:
        """
        Because Sprite.rect "could" be None, but not in our case, this function is only for typing purpose.
        """
        return cast(pygame.Rect, self.rect)

    def get_surface(self) -> pygame.Surface:
        """
        Because Sprite.image "could" be None, but not in our case, this function is only for typing purpose.
        """
        return cast(pygame.Surface, self.image)

    @property
    def world_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.position[0] - self.size[0] // 2,
            self.position[1] - self.size[1] // 2,
            self.size[0],
            self.size[1],
        )

    @property
    def world_bounds(self):
        return WorldObjectBounds(
            self.world_rect[0],
            self.world_rect[0] + self.size[0],
            self.world_rect[1],
            self.world_rect[1] + self.size[1],
        )

    def update_position(self, camera: Camera, screen_size: tuple[int, int]):
        """
        Update device scale based on camera zoom

        ┌──────────────────────────────────────────────────────────┐
        │                                                          │
        │                                                          │
        │                     ┌ do not render                      │
        │                     ▼   ┌──────────────┐                 │
        │                  ┌──────│──────────────│──────┐          │
        │                  │//////│              │//////│          │
        │                  └──────│──────────────│──────┘          │
        │                   ▲     └──────────────┘                 │
        │                   │       ▲                              │
        │                   device  │                              │
        │                           world view                     │
        └──────────────────────────────────────────────────────────┘
         ▲
         └ globale map
        """
        start = time.perf_counter()
        if not self.is_inside_screen:
            end = time.perf_counter()
            self.update_time = end - start
            return
        screen_position = self.game.camera.world_to_screen(self.position, self.game.resolution.size)

        # TODO: cropping to improve perfs
        # self.crop_left = max(0, camera.world_view[0] - self.world_bounds[0])
        # self.crop_right = max(0, self.world_bounds[1] - camera.world_view[1])
        # self.crop_top = max(0, camera.world_view[2] - self.world_bounds[2])
        # self.crop_bottom = max(0, self.world_bounds[3] - camera.world_view[3])

        # cropped_width = self.size[0] - (self.crop_left + self.crop_right)
        # cropped_height = self.size[1] - (self.crop_top + self.crop_bottom)

        # subsurface = self.base_image.subsurface((self.crop_left, self.crop_top, cropped_width, cropped_height))

        subsurface = pygame.transform.scale_by(self.base_image, self.game.camera.zoom)
        self.image = subsurface
        self.rect = self.base_image.get_rect()
        self.rect.center = screen_position

        end = time.perf_counter()
        self.update_time = end - start

    @property
    def is_inside_screen(self) -> bool:
        """Determine if any portion of the object is inside the screen"""
        return (
            self.world_bounds[0] < self.game.camera.world_view[1]
            and self.world_bounds[1] > self.game.camera.world_view[0]
            and self.world_bounds[2] < self.game.camera.world_view[3]
            and self.world_bounds[3] > self.game.camera.world_view[2]
        )

    def draw(self, surface: pygame.Surface) -> None:
        if not self.is_inside_screen:
            return

        # surface.blit(self.get_surface(), (max(self.get_rect()[0], 0), max(self.get_rect()[1], 0)))
        position = self.game.camera.world_to_screen(self.position, self.game.resolution.size)
        rect = self.get_rect().scale_by(self.game.camera.zoom)
        surface.blit(self.get_surface(), (position[0] - rect.width // 2, position[1] - rect.height // 2))
