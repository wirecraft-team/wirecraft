from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING, cast

import pygame

from ..constants import RED
from .assets import SWITCH_DEVICE

if TYPE_CHECKING:
    from ..game import Game
    from .camera import Camera


class Device(pygame.sprite.Sprite):
    def __init__(self, game: Game, world_pos: tuple[float, float], device_type: str):
        super().__init__()
        self.world_pos = world_pos
        self.base_image = SWITCH_DEVICE
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.game = game

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

    def update_zoom(self, camera: Camera):
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
        print(camera.zoom)
        scaled_width = int(self.base_image.get_width() * camera.zoom)
        scaled_height = int(self.base_image.get_height() * camera.zoom)

        # world_rect = (
        #     self.world_pos[0] - scaled_width // 2,
        #     self.world_pos[1] - scaled_height // 2,
        #     scaled_width,
        #     scaled_height,
        # )

        # world_view = (
        #     self.game.camera.x - self.game.resolution.width // 2,
        #     self.game.camera.y - self.game.resolution.height // 2,
        #     self.game.resolution.width,
        #     self.game.resolution.height,
        # )

        # print(world_view)
        # print(world_rect)

        # if world_view[0] < world_rect[0]:
        #     left = 0
        # else:
        #     left = int(((world_view[0] - world_rect[0]) / world_rect[2]) * self.base_image.get_width()) + 10

        # top = 0
        # width = self.base_image.get_width() - left
        # height = self.base_image.get_height() - top

        # crop_left = max(0, self.base_image.get_width() * (world_view[0] - world_rect[0]) // camera.zoom)
        # crop_width = min(
        #     self.base_image.get_width() - crop_left - 1,
        #     self.base_image.get_width() * (world_rect[2] - world_view[2]) // camera.zoom,
        # )
        # print(crop_left, crop_width)
        # subsurface = self.base_image.subsurface(
        #     left,
        #     top,
        #     width,
        #     height,
        #     # max(0, view_left - sprite_left),
        #     # max(0, view_top - sprite_top),
        #     # 1000,
        #     # 1000,
        # )
        start = time.perf_counter()
        self.image = pygame.transform.scale_by(
            self.base_image, camera.zoom
        )  # pygame.transform.scale(subsurface, (scaled_width, scaled_height))
        end = time.perf_counter()
        print(end - start)
        self.rect = pygame.Rect(0, 0, scaled_width, scaled_height)

    def update_position(self, camera: Camera, screen_size: tuple[int, int]):
        """Update device position based on camera"""

        # if world_view[0] < world_rect[0]:
        # else:
        #     left = int(((world_view[0] - world_rect[0]) / world_rect[2]) * self.base_image.get_width()) + 10

        world_view = self.game.camera.world_view
        left = max(world_view[0], self.world_rect[0]) - self.world_rect[0]
        top = max(world_view[1], self.world_rect[1]) - self.world_rect[1]

        print(left)

        width = self.base_image.get_width() - left
        height = self.base_image.get_height() - top

        subsurface = self.base_image.subsurface(
            left,
            top,
            width,
            height,
            # max(0, view_left - sprite_left),
            # max(0, view_top - sprite_top),
            # 1000,
            # 1000,
        )
        start = time.perf_counter()
        self.image = pygame.transform.scale_by(
            subsurface, camera.zoom
        )  # pygame.transform.scale(subsurface, (scaled_width, scaled_height))
        end = time.perf_counter()
        print(end - start)
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        screen_pos = camera.world_to_screen(self.world_pos, screen_size)
        self.get_rect().center = (int(screen_pos[0]), int(screen_pos[1]))

    def offset_rec(self):
        rect = self.get_rect()
        return (rect[0] + 10, rect[1] + 10, rect[2], rect[3])

    @property
    def world_rect(self):
        # scaled_width = int(self.base_image.get_width() * self.game.camera.zoom)
        # scaled_height = int(self.base_image.get_height() * self.game.camera.zoom)

        return (
            self.world_pos[0] - self.base_image.get_width() // 2,
            self.world_pos[1] - self.base_image.get_height() // 2,
            self.base_image.get_width(),
            self.base_image.get_height(),
        )

    @property
    def inside_screen(self):
        """
        This function determine if the sprite is inside the screen or not.
        """
        left_view_border = self.game.camera.world_view[0]
        right_view_border = self.game.camera.world_view[0] + self.game.camera.world_view[2]
        top_view_border = self.game.camera.world_view[1]
        bottom_view_border = self.game.camera.world_view[1] + +self.game.camera.world_view[3]

        left_rect_border = self.world_rect[0]
        right_rect_border = self.world_rect[0] + self.world_rect[2]
        top_rect_border = self.world_rect[1]
        bottom_rect_border = self.world_rect[1] + +self.world_rect[3]

        # fmt: off
        return (
            left_rect_border < right_view_border
        ) and (
            right_rect_border > left_view_border
        ) and (
            top_rect_border < bottom_view_border
        ) and (
            bottom_rect_border > top_view_border
        )
        # fmt: on

    def draw(self, surface: pygame.Surface) -> None:
        # draw the rect in red so we can see it
        print(self.inside_screen)
        if not self.inside_screen:
            return
        if True or os.environ.get(
            "DEBUG"
        ):  # for now, nothing has been decided about a "DEBUG" mode. Could be discussed later.
            pygame.draw.rect(surface, RED, self.get_rect())
        surface.blit(self.get_surface(), self.offset_rec())
