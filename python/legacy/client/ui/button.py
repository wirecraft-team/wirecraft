from __future__ import annotations

from collections.abc import Callable

import pygame


class Button:
    def __init__(
        self,
        position: tuple[float, float],
        size: tuple[float, float],
        action: Callable[[], None],
        image: pygame.Surface,
    ) -> None:
        self.position = position
        self.size = size
        self.action = action
        self.image = image

    def draw(self, surface: pygame.Surface) -> None:
        """Draws a button according to the position and size attributes. Coordinates are screen coordinates. (top left corner is (0, 0))"""
        self.image = pygame.transform.scale(self.image, self.size)
        surface.blit(self.image, self.position)
