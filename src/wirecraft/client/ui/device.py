from __future__ import annotations

from typing import TYPE_CHECKING

from wirecraft.client.ui.extended_sprite import ExtendedSprite

from . import Assets

if TYPE_CHECKING:
    from ..game import Game


class Device(ExtendedSprite):
    def __init__(self, game: Game, position: tuple[int, int], device_type: str):
        """
        Position is the point in the world map that refer to the center of the device.
        """
        super().__init__(game, position, Assets.SWITCH_DEVICE)
