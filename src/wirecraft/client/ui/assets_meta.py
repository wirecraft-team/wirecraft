"""
assets_meta.py contains the "secrets" classes that make the assets.py file work "magically".
This code is "private" in the sense that it is not meant to be used outside assets.py.

This code use Metaclasses and Descriptors. These are advanced Python features that I will not explain here to avoid
verbose explanations.
"""

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
    """
    A metaclass that defined the underlying class as a singleton (only one instance of the class can exist) and also
    add a attribute to the class that will store all the assets loaders.

    The assets loaders are the instances of the Asset class that are defined in the class body.
    The class also provide a method to load all the assets.
    """

    def __new__(cls, name: str, bases: tuple[Any], dct: dict[str, Any]):
        dct["__assets_loaders__"] = []
        return super().__new__(cls, name, bases, dct)

    def load_assets(cls):  # noqa: N805 (false positive...)
        for asset_loader in getattr(cls, "__assets_loaders__"):
            asset_loader.load()


class Asset:
    """
    An Asset is a descriptor that will lazy-load the asset on access-time.
    That means that the asset is not loaded at definition time but when it is accessed for the first time

    Alternatively, the Asset can be loaded using the Descriptor load() method, but this method is not easily accessible.
    You should use the AssetsMeta.load_assets() method to load all the assets at once.
    """

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


class SvgAsset(Asset):
    """
    Same as Asset but to load SVG files (with a specific size).
    """

    def __init__(self, filename: str, size: tuple[int, int]):
        super().__init__(filename)
        self.size = size

    def load(self):
        if not self.is_loaded:
            self._loaded_asset = pygame.image.load_sized_svg(assets_dir / self.filename, self.size).convert_alpha()
            print(f"Loaded {self.filename}")
        else:
            print(f"{self.filename} is already loaded !")
