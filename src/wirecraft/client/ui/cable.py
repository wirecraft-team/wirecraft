from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from ..constants import RED

if TYPE_CHECKING:
    from .camera import Camera
    from .window import Resolution

from wirecraft.shared_context import server_var


class Cable:
    def __init__(
        self,
        id_device1: int,
        port_device1: int,
        id_device2: int,
        port_device2: int,
        db_id: int,
    ) -> None:
        self.id_device1 = id_device1
        self.port_device1 = port_device1
        self.id_device2 = id_device2
        self.port_device2 = port_device2
        self.db_id = db_id

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
        # TODO fix position of the cable
        pygame.draw.line(
            surface,
            RED,
            camera.world_to_screen(
                (
                    server_var.get().get_device_pos(self.id_device1)[0]
                    + server_var.get().get_port_pos(self.port_device1, self.id_device1)[0],
                    server_var.get().get_device_pos(self.id_device1)[1]
                    + server_var.get().get_port_pos(self.port_device1, self.id_device1)[1],
                ),
                resolution.size,
            ),
            camera.world_to_screen(
                (
                    server_var.get().get_device_pos(self.id_device2)[0]
                    + server_var.get().get_port_pos(self.port_device2, self.id_device2)[0],
                    server_var.get().get_device_pos(self.id_device2)[1]
                    + server_var.get().get_port_pos(self.port_device2, self.id_device2)[1],
                ),
                resolution.size,
            )
            if self.id_device2 > 0
            else pygame.mouse.get_pos(),
            width=5,
        )
