from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from ..constants import RED

if TYPE_CHECKING:
    from .camera import Camera
    from .window import Resolution


class Cable:
    def __init__(self, start: tuple[float, float], end: tuple[float, float]):
        self.start = start
        self.end = end
        self.ended = False
        # Store world coordinates for consistent positioning
        self.start_world: tuple[float, float] | None = None
        self.end_world: tuple[float, float] | None = None

    def update_position(self, camera: Camera, resolution: Resolution) -> None:
        """Update cable position based on camera movement

        If the cable is connected to devices (ended=True), both points should be
        updated using world coordinates. If the cable is being placed, only the start
        point should be updated (end point follows mouse).
        """
        # screen_size = resolution.size  # Get the tuple from Resolution object

        # First time update: calculate and store world coordinates
        if self.start_world is None:
            # self.start_world = camera.screen_to_world(self.start, screen_size)  # TODO: use int
            pass
        if self.ended and self.end_world is None:
            # self.end_world = camera.screen_to_world(self.end, screen_size)  # TODO: use int
            pass

        # Update start point screen position
        # self.start = camera.world_to_screen(self.start_world, screen_size)  # TODO: use int

        # Update end point screen position only if cable is complete
        if self.ended and self.end_world is not None:
            # self.end = camera.world_to_screen(self.end_world, screen_size)  # TODO: use int
            pass

    def update_zoom(self, camera: Camera) -> None:
        pass

    def draw(self, surface: pygame.Surface, camera: Camera, resolution: Resolution) -> None:
        pygame.draw.line(surface, RED, self.start, self.end, 5)
