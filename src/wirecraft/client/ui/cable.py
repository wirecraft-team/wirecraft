from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import numpy as np
import pygame

from ..constants import RED
from ..ui import Assets

if TYPE_CHECKING:
    from ..game import Game
    from .camera import Camera
    from .window import Resolution


@dataclass
class Cable:
    id_device1: int
    port_device1: int
    id_device2: int
    port_device2: int
    db_id: int
    game: Game
    start_offset: tuple[int, int] = (0, 0)
    end_offset: tuple[int, int] = (0, 0)

    def update_zoom(self, camera: Camera) -> None:
        pass

    def initiate_position(self, camera: Camera):
        self.start_offset = self.get_center_of_red(self.port_device1)
        self.end_offset = self.get_center_of_red(self.port_device2)

    def draw(self, surface: pygame.Surface, camera: Camera, resolution: Resolution) -> None:
        # TODO use a map to get pos from id
        dev_1_pos = next(device.world_rect for device in self.game.devices if device.db_id == self.id_device1)
        port_1_pos = (dev_1_pos[0] + self.start_offset[0], dev_1_pos[1] + self.start_offset[1])
        if self.port_device2 <= 0:
            port_2_pos = camera.screen_to_world(pygame.mouse.get_pos(), resolution.size)
        else:
            dev_2_pos = next(device.world_rect for device in self.game.devices if device.db_id == self.id_device2)
            port_2_pos = (dev_2_pos[0] + self.end_offset[0], dev_2_pos[1] + self.end_offset[1])
        pygame.draw.line(
            surface,
            RED,
            camera.world_to_screen(
                port_1_pos,
                resolution.size,
            ),
            camera.world_to_screen(
                port_2_pos,
                resolution.size,
            ),
            width=5,
        )

    def get_center_of_red(self, port_id: int) -> tuple[int, int]:
        if port_id <= 0:
            return (0, 0)
        pixel_array = pygame.surfarray.pixels3d(Assets.SWITCH_DEVICE.mask)  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        # Extract the red channel
        red_channel: np.ndarray[Any, Any] = pixel_array[:, :, 0]
        blue_channel: np.ndarray[Any, Any] = pixel_array[:, :, 2]
        green_channel: np.ndarray[Any, Any] = pixel_array[:, :, 1]

        # Find where red channel equals target_value
        x_coords, y_coords = np.where((red_channel == port_id) & (blue_channel == 0) & (green_channel == 0))

        # Find the bounding box and calculate the center
        x_min, x_max = x_coords.min(), x_coords.max()
        y_min, y_max = y_coords.min(), y_coords.max()

        center_x = (x_min + x_max) // 2
        center_y = (y_min + y_max) // 2
        return (int(center_x), int(center_y))
