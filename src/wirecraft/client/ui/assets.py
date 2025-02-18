from .assets_meta import Asset, AssetsMeta, SvgAsset


class Assets(metaclass=AssetsMeta):
    # Be careful about the size of the assets, the ratio shoul be the same as the asset
    SWITCH_DEVICE = SvgAsset("switch.svg", (1470, 220), mask=True, positions={i: (i, 0, 0) for i in range(1, 9)})
    PC_DEVICE = SvgAsset("pc.svg", (940, 1570), mask=True, positions={i: (i, 0, 0) for i in range(1, 2)})
    CLOSE_BUTTON = Asset("close.png")
    INVENTORY_BUTTON = Asset("inventory.png")
