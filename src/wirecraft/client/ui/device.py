from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pygame

from ..constants import RED
from .assets import SWITCH_DEVICE

if TYPE_CHECKING:
    from .camera import Camera


class Device(pygame.sprite.Sprite):
    def __init__(self, world_pos: tuple[float, float], device_type: str):
        super().__init__()
        self.world_pos = world_pos
        self.base_image = SWITCH_DEVICE
        self.image = self.base_image
        self.rect = self.image.get_rect()

    def update_zoom(self, camera: Camera):
        """Update device scale based on camera zoom"""
        scaled_width = int(self.base_image.get_width() * camera.zoom)
        scaled_height = int(self.base_image.get_height() * camera.zoom)
        self.image = pygame.transform.scale(self.base_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()

    def update_position(self, camera: Camera, screen_size: tuple[int, int]):
        """Update device position based on camera"""
        screen_pos = camera.world_to_screen(self.world_pos, screen_size)
        self.rect.center = (int(screen_pos[0]), int(screen_pos[1]))

    def draw(self, surface: pygame.Surface) -> None:
        # draw the rect in red so we can see it
        if os.environ.get("DEBUG"):  # for now, nothing has been decided about a "DEBUG" mode. Could be discussed later.
            pygame.draw.rect(surface, RED, self.rect)
        surface.blit(self.image, self.rect)
