from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Camera:
    x: float
    y: float
    zoom: float
    min_zoom: float = 0.3
    max_zoom: float = 10

    def screen_to_world(self, screen_pos: tuple[float, float], screen_size: tuple[int, int]) -> tuple[float, float]:
        """Convert screen coordinates to world coordinates
        screen coordinates are relative to the top left corner of the screen, world coordinates are relative to the center of the screen

        Args:
            screen_pos: the position on the screen
            screen_size: the size of the screen

        Returns:
            the position in the world
        """
        screen_center = (screen_size[0] / 2, screen_size[1] / 2)
        rel_x = (screen_pos[0] - screen_center[0]) / self.zoom
        rel_y = (screen_pos[1] - screen_center[1]) / self.zoom
        return (rel_x + self.x, rel_y + self.y)

    def world_to_screen(self, world_pos: tuple[float, float], screen_size: tuple[int, int]) -> tuple[float, float]:
        """Convert world coordinates to screen coordinates
        screen coordinates are relative to the top left corner of the screen, world coordinates are relative to the center of the screen

        Args:
            world_pos: the position in the world
            screen_size: the size of the screen

        Returns:
            the position on the screen
        """
        screen_center = (screen_size[0] / 2, screen_size[1] / 2)
        rel_x = (world_pos[0] - self.x) * self.zoom
        rel_y = (world_pos[1] - self.y) * self.zoom
        return (screen_center[0] + rel_x, screen_center[1] + rel_y)

    def adjust_zoom(self, delta: float, mouse_pos: tuple[int, int], screen_size: tuple[int, int]):
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
        old_zoom = self.zoom
        self.zoom = max(self.min_zoom, min(self.max_zoom, self.zoom + delta))
        if old_zoom == self.zoom:
            return
        new_screen_pos = self.world_to_screen(old_world_pos, screen_size)
        self.x -= (mouse_pos[0] - new_screen_pos[0]) / self.zoom
        self.y -= (mouse_pos[1] - new_screen_pos[1]) / self.zoom
