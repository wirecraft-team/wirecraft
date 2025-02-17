"""
assets_meta.py contains the "secrets" classes that make the assets.py file work "magically".
This code is "private" in the sense that it is not meant to be used outside assets.py.

This code use Metaclasses and Descriptors. These are advanced Python features that I will not explain here to avoid
verbose explanations.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, cast, overload

import pygame

from ..utils import SingletonMeta

if TYPE_CHECKING:
    from .assets import Assets

    type PositionsColorsMapT = dict[Any, tuple[int, int, int]]
    type ComputedPositionsT = dict[Any, tuple[int, int]]

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


@dataclass
class SimpleAsset:
    surface: pygame.Surface
    mask: None = None
    ports: None = None


@dataclass
class MaskedAsset:
    surface: pygame.Surface
    mask: pygame.Surface
    ports: PositionsColorsMapT


class Asset[M]:
    """
    An Asset is a descriptor that will lazy-load the asset on access-time.
    That means that the asset is not loaded at definition time but when it is accessed for the first time

    Alternatively, the Asset can be loaded using the Descriptor load() method, but this method is not easily accessible.
    You should use the AssetsMeta.load_assets() method to load all the assets at once.
    """

    @overload
    def __init__(
        self: Asset[SimpleAsset], filename: str, mask: Literal[False] = False, positions: None = None
    ) -> None: ...
    @overload
    def __init__(
        self: Asset[MaskedAsset], filename: str, mask: Literal[True], positions: PositionsColorsMapT
    ) -> None: ...

    def __init__(self, filename: str, mask: bool = False, positions: PositionsColorsMapT | None = None):
        self.filename = filename
        self._loaded_asset: pygame.Surface | None = None
        self.mask = mask
        self._loaded_mask: pygame.Surface | None = None
        self._positions = positions
        self._computed_positions = None

    def __set_name__(self, owner: Assets, name: str):
        getattr(owner, "__assets_loaders__").append(self)

    @property
    def is_loaded(self):
        return self._loaded_asset is not None

    def load(self):
        if not self.is_loaded:
            self._loaded_asset = pygame.image.load(assets_dir / self.filename).convert_alpha()
            if self.mask:
                self._loaded_mask = pygame.image.load(assets_dir / f"mask_{self.filename}")
                # TODO: load the ports positions
            print(f"Loaded {self.filename}")
        else:
            print(f"{self.filename} is already loaded !")

    def _get_center_from_color(self, color: tuple[int, int, int]):
        # TODO: calculate the center of the color here depending of the given color
        pass

    def __get__(self, instance: Assets | None, owner: type[Assets]) -> M:
        if not self.is_loaded:
            self.load()

        if TYPE_CHECKING:
            assert self._loaded_asset is not None

        if self.mask:
            if TYPE_CHECKING:
                assert self._loaded_mask is not None
                assert self._positions is not None

            return cast(M, MaskedAsset(self._loaded_asset, self._loaded_mask, self._positions))
        return cast(M, SimpleAsset(self._loaded_asset))


class SvgAsset[M](Asset[M]):
    """
    Same as Asset but to load SVG files (with a specific size).
    """

    @overload
    def __init__(
        self: SvgAsset[SimpleAsset],
        filename: str,
        size: tuple[int, int],
        mask: Literal[False] = False,
        positions: None = None,
    ) -> None: ...
    @overload
    def __init__(
        self: SvgAsset[MaskedAsset],
        filename: str,
        size: tuple[int, int],
        mask: Literal[True],
        positions: PositionsColorsMapT,
    ) -> None: ...

    def __init__(
        self, filename: str, size: tuple[int, int], mask: bool = False, positions: PositionsColorsMapT | None = None
    ):
        super().__init__(filename, mask, positions)  # type: ignore  # TODO
        self.size = size

    def load(self):
        if not self.is_loaded:
            self._loaded_asset = pygame.image.load_sized_svg(assets_dir / self.filename, self.size).convert_alpha()
            if self.mask:
                self._loaded_mask = pygame.image.load_sized_svg(assets_dir / f"mask_{self.filename}", self.size)
                # TODO: load the ports positions
            print(f"Loaded {self.filename}")
        else:
            print(f"{self.filename} is already loaded !")
