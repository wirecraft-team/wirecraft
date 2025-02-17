from dataclasses import dataclass

import pygame

from ..constants import BLACK, GREY
from . import Assets


@dataclass
class Resolution:
    width: int
    height: int

    @property
    def size(self) -> tuple[int, int]:
        return (self.width, self.height)


class Window:
    def __init__(self, position: tuple[float, float], size: tuple[float, float], title: str, data: str) -> None:
        self.position = position
        self.size = size
        self.title = title
        self.data = data

    def update_pos(self, index: int, resolution: Resolution) -> None:
        """This function should only be called for device properties windows, and should be modified when they are properly implemented"""
        offset = (index) * resolution.width / 7.5
        self.position = (resolution.width - self.size[0] - 20, 20 + offset)
        self.size = (resolution.width / 5, resolution.height / 5)

    def draw(self, surface: pygame.Surface) -> None:
        """Draws a windows according to the position and size attributes. Coordinates are screen coordinates. (top left corner is (0, 0))"""
        window = pygame.Surface(self.size)
        window.fill(GREY)
        close_button = pygame.transform.scale(Assets.CLOSE_BUTTON.surface, (25, 25))
        pygame.draw.rect(window, BLACK, (0, 0, self.size[0], self.size[1]), 5)
        surface.blit(window, self.position)
        surface.blit(close_button, (self.position[0] + self.size[0] - 40, self.position[1] + 10))
        title = pygame.font.Font(None, 50).render(self.title, True, BLACK)
        surface.blit(title, (self.position[0] + 10, self.position[1] + 10))
        text = pygame.font.Font(None, 50).render(self.data, True, BLACK)
        surface.blit(text, (self.position[0] + 10, self.position[1] + 50))
