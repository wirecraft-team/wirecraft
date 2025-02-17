from .assets_meta import Asset, AssetsMeta, SvgAsset


class Assets(metaclass=AssetsMeta):
    SWITCH_MASK = Asset("switch_mask.png")
    SWITCH_DEVICE = SvgAsset("switch.svg", (18910, 1660))
    PC_DEVICE = Asset("pc.png")
    CLOSE_BUTTON = Asset("close.png")
    INVENTORY_BUTTON = Asset("inventory.png")
