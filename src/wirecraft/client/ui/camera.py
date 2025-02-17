from __future__ import annotations

from typing import TYPE_CHECKING, Literal, NamedTuple

if TYPE_CHECKING:
    from ..game import Game


class ObjectBounds(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int


class Camera:
    """
      x: position of the center of the screen
      y: position of the center of the screen


      Imagine the map being a 5000*5000 pixels.
      Our camera can only view 1080*1920 pixels, and the center of this "view" scare is at the position (x, y) relative to
      the entire map center.

     ┌──────────────────────────────────┐
     │                                  │
     │                                  │
     │                  ┌────────────┐  │
     │                  │            │  │
     │                  │     x,y    │  │
     │                  │            │  │
     │                  └────────────┘  │
     │                                  │
     │                                  │
     │                                  │
    ^│                                  │
    |│                                  │
    y└──────────────────────────────────┘
      x->
    """

    def __init__(self, game: Game, x: int = 0, y: int = 0, initial_zoom: int = 10):
        self.x: int = x
        self.y: int = y
        self.zoom_value = initial_zoom
        self.game = game

    @property
    def world_view(self) -> ObjectBounds:
        """
        This return a tuple of (x_min, x_max, y_min, y_max) relative to the world map.
        ┌─────────────────────────────┐
        │                             │
        │ x_min    x_max              │
        │ ▼        ▼                  │
        │ ┌────────┐◄ y_min           │
        │ │        │                  │
        │ │        │                  │
        │ └────────┘◄ y_max           │
        │                             │
        └─────────────────────────────┘
        """
        return ObjectBounds(
            *map(
                int,
                (
                    self.x - (self.game.resolution.width / 2) / self.zoom,
                    self.x + (self.game.resolution.width / 2) / self.zoom,
                    self.y - (self.game.resolution.height / 2) / self.zoom,
                    self.y + (self.game.resolution.height / 2) / self.zoom,
                ),
            )
        )

    def screen_to_world(self, screen_pos: tuple[int, int], screen_size: tuple[int, int]) -> tuple[int, int]:
        """Convert screen coordinates to world coordinates
        screen coordinates are relative to the top left corner of the screen, world coordinates are relative to the center of the screen

        Args:
            screen_pos: the position on the screen
            screen_size: the size of the screen

        Returns:
            the position in the world
        """
        screen_center = (screen_size[0] // 2, screen_size[1] // 2)
        rel_x = int((screen_pos[0] - screen_center[0]) / self.zoom)
        rel_y = int((screen_pos[1] - screen_center[1]) / self.zoom)
        return (rel_x + self.x, rel_y + self.y)

    def world_to_screen(self, world_pos: tuple[int, int], screen_size: tuple[int, int]) -> tuple[int, int]:
        """Convert world coordinates to screen coordinates
        screen coordinates are relative to the top left corner of the screen, world coordinates are relative to the center of the screen

        Args:
            world_pos: the position in the world
            screen_size: the size of the screen

        Returns:
            the position on the screen
        """
        screen_center = (screen_size[0] // 2, screen_size[1] // 2)
        rel_x = int((world_pos[0] - self.x) * self.zoom)
        rel_y = int((world_pos[1] - self.y) * self.zoom)
        return (screen_center[0] + rel_x, screen_center[1] + rel_y)

    @property
    def zoom(self):
        # return 1
        return self.zoom_value / 100

    @property
    def zoom_value(self):
        return self._zoom_value

    @zoom_value.setter
    def zoom_value(self, value: int):
        self._zoom_value = max(3, min(100, value))

    def zoom_out(self, mouse_pos: tuple[int, int], screen_size: tuple[int, int]):
        return self._tick_zoom("out", mouse_pos, screen_size)

    def zoom_in(self, mouse_pos: tuple[int, int], screen_size: tuple[int, int]):
        return self._tick_zoom("in", mouse_pos, screen_size)

    def _tick_zoom(self, mode: Literal["in", "out"], mouse_pos: tuple[int, int], screen_size: tuple[int, int]):
        v = 1
        if mode == "out":
            v = -v
        return self.set_zoom(self.zoom_value + v, mouse_pos, screen_size)

    def set_zoom(self, zoom_value: int, mouse_pos: tuple[int, int], screen_size: tuple[int, int]):
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

        old_zoom = self.zoom_value
        self.zoom_value = zoom_value
        if self.zoom_value == old_zoom:
            return False

        new_screen_pos = self.world_to_screen(old_world_pos, screen_size)
        self.x -= int((mouse_pos[0] - new_screen_pos[0]) / self.zoom)
        self.y -= int((mouse_pos[1] - new_screen_pos[1]) / self.zoom)
        return True
