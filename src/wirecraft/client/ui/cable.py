from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
import pygame

from ..constants import RED
from ..ui.assets import SWITCH_MASK

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

    def update_position(self, camera: Camera, resolution: Resolution) -> None:
        """Update cable position based on camera movement

        If the cable is connected to devices (ended=True), both points should be
        updated using world coordinates. If the cable is being placed, only the start
        point should be updated (end point follows mouse).
        """

    # this function looks unnecessary as it works fine without it but to be confirmed
    # screen_size = resolution.size  # Get the tuple from Resolution object
    # screen_size = resolution.size  # Get the tuple from Resolution object

    #
    ## First time update: calculate and store world coordinates
    # if self.start_world is None:
    #    self.start_world = camera.screen_to_world(self.start, screen_size)
    # if self.ended and self.end_world is None:
    #    self.end_world = camera.screen_to_world(self.end, screen_size)
    #
    ## Update start point screen position
    # self.start = camera.world_to_screen(self.start_world, screen_size)
    #
    ## Update end point screen position only if cable is complete
    # if self.ended and self.end_world is not None:
    #    self.end = camera.world_to_screen(self.end_world, screen_size)

    def update_zoom(self, camera: Camera) -> None:
        pass

    def draw(self, surface: pygame.Surface, camera: Camera, resolution: Resolution) -> None:
        # TODO use a map to get pos from id
        # TODO don't compute this every frame
        dev_1_pos = next(device.world_rect for device in self.game.devices if device.db_id == self.id_device1)
        port_1_pos = self.get_center_of_red(self.port_device1)
        start_x = dev_1_pos[0] + port_1_pos[0]
        start_y = dev_1_pos[1] + port_1_pos[1]
        if self.id_device2 > 0 and self.port_device2 > 0:
            dev_2_pos = next(device.world_rect for device in self.game.devices if device.db_id == self.id_device2)
            port_2_pos = self.get_center_of_red(self.port_device2)

            end_x = dev_2_pos[0] + port_2_pos[0]
            end_y = dev_2_pos[1] + port_2_pos[1]
        else:
            end_x, end_y = pygame.mouse.get_pos()
        pygame.draw.line(
            surface,
            RED,
            camera.world_to_screen(
                (start_x, start_y),
                resolution.size,
            ),
            camera.world_to_screen(
                (end_x, end_y),
                resolution.size,
            )
            if self.id_device2 > 0 and self.port_device2 > 0
            else (end_x, end_y),
            width=5,
        )

    def get_center_of_red(self, port_id: int) -> tuple[int, int]:
        pixel_array = pygame.surfarray.pixels3d(SWITCH_MASK)  # type: ignore
        # Extract the red channel
        red_channel: np.ndarray = pixel_array[:, :, 0]  # type: ignore
        blue_channel: np.ndarray = pixel_array[:, :, 2]  # type: ignore
        green_channel: np.ndarray = pixel_array[:, :, 1]  # type: ignore

        # Find where red channel equals target_value
        x_coords, y_coords = np.where((red_channel == port_id) & (blue_channel == 0) & (green_channel == 0))

        # Find the bounding box and calculate the center
        x_min, x_max = x_coords.min(), x_coords.max()
        y_min, y_max = y_coords.min(), y_coords.max()

        center_x = (x_min + x_max) // 2
        center_y = (y_min + y_max) // 2
        return (int(center_x), int(center_y))
