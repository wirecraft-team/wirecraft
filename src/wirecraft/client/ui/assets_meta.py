from __future__ import annotations

from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pygame

from ..utils import SingletonMeta

if TYPE_CHECKING:
    from .assets import Assets

# Check for assets in the package if installed
assets_dir = Path(str(files("wirecraft").joinpath("assets")))

# Otherwise check on the local directory if executed in dev environnement
if not assets_dir.exists():
    assets_dir = Path("./assets")


class AssetsMeta(SingletonMeta):
    def __new__(cls, name: str, bases: tuple[Any], dct: dict[str, Any]):
        dct["__assets_loaders__"] = []
        return super().__new__(cls, name, bases, dct)

    def load_assets(cls):  # noqa: N805 (false positive...)
        for asset_loader in getattr(cls, "__assets_loaders__"):
            asset_loader.load()


class Asset:
    def __init__(self, filename: str):
        self.filename = filename
        self._loaded_asset: pygame.Surface | None = None

    def __set_name__(self, owner: Assets, name: str):
        getattr(owner, "__assets_loaders__").append(self)

    @property
    def is_loaded(self):
        return self._loaded_asset is not None

    def load(self):
        if not self.is_loaded:
            self._loaded_asset = pygame.image.load(assets_dir / self.filename).convert_alpha()
            print(f"Loaded {self.filename}")
        else:
            print(f"{self.filename} is already loaded !")

    def __get__(self, instance: Assets | None, owner: type[Assets]) -> pygame.Surface:
        if not self.is_loaded:
            self.load()

        if TYPE_CHECKING:
            assert self._loaded_asset is not None

        return self._loaded_asset
