from .assets_meta import Asset, AssetsMeta, SvgAsset


class Assets(metaclass=AssetsMeta):
    SWITCH_DEVICE = SvgAsset("switch.svg", (18910, 1660), mask=True, ports={1: (1, 0, 0)})
    PC_DEVICE = Asset("pc.png")
    CLOSE_BUTTON = Asset("close.png")
    INVENTORY_BUTTON = Asset("inventory.png")
