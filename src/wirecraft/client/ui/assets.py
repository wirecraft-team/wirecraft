from .assets_meta import Asset, AssetsMeta, SvgAsset


class Assets(metaclass=AssetsMeta):
    SWITCH_DEVICE = SvgAsset("switch.svg", (18910, 1660), mask=True, positions={i: (i, 0, 0) for i in range(7)})
    PC_DEVICE = Asset("pc.png")
    CLOSE_BUTTON = Asset("close.png")
    INVENTORY_BUTTON = Asset("inventory.png")
