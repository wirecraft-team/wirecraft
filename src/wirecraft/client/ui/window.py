from dataclasses import dataclass
from enum import Enum

import pygame

from ..constants import BLACK, GREY
from .assets import CLOSE_BUTTON


@dataclass
class Resolution:
    width: int
    height: int

    @property
    def size(self) -> tuple[int, int]:
        return (self.width, self.height)


class WindowType(Enum):
    POPUP = 1
    TASK = 2
    INVENTORY = 3


class Window:
    def __init__(
        self, position: tuple[float, float], size: tuple[float, float], title: str, data: str, type: WindowType
    ) -> None:
        self.position = position
        self.size = size
        self.title = title
        self.data = data
        self.type = type
        self.time = 300

    def update_pos(self, index: int, resolution: Resolution) -> None:
        """This function should only be called for device properties windows, and should be modified when they are properly implemented"""
        offset = (index) * resolution.width / 7.5
        self.position = (resolution.width - self.size[0] - 20, 20 + offset)
        self.size = (resolution.width / 5, resolution.height / 5)

    def draw(self, surface: pygame.Surface) -> None:
        """Draws a windows according to the position and size attributes. Coordinates are screen coordinates. (top left corner is (0, 0))"""
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
