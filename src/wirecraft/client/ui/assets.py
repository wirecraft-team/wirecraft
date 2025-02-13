from .assets_meta import Asset, AssetsMeta


class Assets(metaclass=AssetsMeta):
    SWITCH_DEVICE = Asset("switch.png")
    # SWITCH_DEVICE = pygame.image.load_sized_svg(f"switch.svg", (18910, 1660))
    PC_DEVICE = Asset("pc.png")
    CLOSE_BUTTON = Asset("close.png")
    INVENTORY_BUTTON = Asset("inventory.png")
