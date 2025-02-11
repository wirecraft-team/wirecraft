from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from .camera import ObjectBounds

if TYPE_CHECKING:
    from ..game import Game
    from .camera import Camera


class ExtendedSprite(pygame.sprite.Sprite):
    def __init__(self, game: Game, position: tuple[int, int], image: pygame.Surface):
        """
        Position is the point in the world map that refer to the center of the device.
        """
        super().__init__()
        self.game = game
        self.position: tuple[int, int] = position
        self.base_image = image.convert_alpha()  # TODO: convert alpha from the beginning
        self.size = (image.get_width(), image.get_height())

    def get_surface(self) -> pygame.Surface:
        if TYPE_CHECKING:
            assert isinstance(self.image, pygame.Surface)
        return self.image

    @property
    def screen_rect(self) -> pygame.Rect:
        """
        Return the rect of the sprite relative to the screen.
        """
        if TYPE_CHECKING:
            assert isinstance(self.rect, pygame.Rect)
        return self.rect

    @property
    def screen_bounds(self) -> ObjectBounds:
        """
        TODO: don't use this, as it is not ready guys
        Return bounds relative to the screen.
        """
        return ObjectBounds(0, 0, 0, 0)  # TODO

    @property
    def world_rect(self) -> pygame.Rect:
        """
        Return the rect of the sprite relative to the world.
        """
        return pygame.Rect(
            self.position[0] - self.size[0] // 2,
            self.position[1] - self.size[1] // 2,
            self.size[0],
            self.size[1],
        )

    @property
    def world_bounds(self):
        """
        Return the bounds of the sprite relative to the world.
        """
        return ObjectBounds(
            self.world_rect[0],
            self.world_rect[0] + self.size[0],
            self.world_rect[1],
            self.world_rect[1] + self.size[1],
        )

    @property
    def screen_position(self) -> tuple[int, int]:
        """
        The coordinate of the center of the device relative to the screen.
        """
        return self.game.camera.world_to_screen(self.position, self.game.resolution.size)

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
        if not self.is_inside_screen:
            return

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
        self.rect = self.base_image.get_rect().scale_by(self.game.camera.zoom)
        self.rect.center = self.screen_position

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
        surface.blit(self.get_surface(), self.screen_rect)
