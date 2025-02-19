from __future__ import annotations

from typing import TYPE_CHECKING

from wirecraft.client.ui.extended_sprite import ExtendedSprite

from . import Assets

if TYPE_CHECKING:
    from ..game import Game


class Device(ExtendedSprite):
    def __init__(self, game: Game, position: tuple[int, int], device_type: str, db_id: int):
        """
        Position is the point in the world map that refer to the center of the device.
        """
        match device_type:
            case "switch":
                asset = Assets.SWITCH_DEVICE
            case "pc":
                asset = Assets.PC_DEVICE
            case _:
                raise ValueError(f"Unknown device type: {device_type}")
        super().__init__(game, position, asset.surface)
        self.asset = asset
        self.db_id = db_id
