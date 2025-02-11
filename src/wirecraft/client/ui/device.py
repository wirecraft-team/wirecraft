from __future__ import annotations

from typing import TYPE_CHECKING

from wirecraft.client.ui.extended_sprite import ExtendedSprite

from .assets import SWITCH_DEVICE

if TYPE_CHECKING:
    from ..game import Game


class Device(ExtendedSprite):
    def __init__(self, game: Game, position: tuple[int, int], device_type: str, db_id: int):
        """
        Position is the point in the world map that refer to the center of the device.
        """
        super().__init__(game, position, SWITCH_DEVICE)
        self.db_id = db_id
