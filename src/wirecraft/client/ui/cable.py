from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pygame

from ..constants import RED

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

    def update_zoom(self) -> None:
        pass

    def initiate_position(self):
        start_asset = next(device for device in self.game.devices if device.db_id == self.id_device1).asset
        end_asset = (
            next(device for device in self.game.devices if device.db_id == self.id_device2).asset
            if self.port_device2 > 0
            else None
        )
        self.start_offset = start_asset.positions[self.port_device1]
        self.end_offset = end_asset.positions[self.port_device2] if end_asset else (0, 0)

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
