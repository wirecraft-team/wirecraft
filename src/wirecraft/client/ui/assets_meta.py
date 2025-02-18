"""
assets_meta.py contains the "secrets" classes that make the assets.py file work "magically".
This code is "private" in the sense that it is not meant to be used outside assets.py.

This code use Metaclasses and Descriptors. These are advanced Python features that I will not explain here to avoid
verbose explanations.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, cast, overload

import numpy as np
import pygame

from ..utils import SingletonMeta

if TYPE_CHECKING:
    from .assets import Assets

    type PositionsColorsMapT = dict[Any, tuple[int, int, int]]
    type ComputedPositionsT = dict[Any, tuple[int, int]]

logger = logging.getLogger(__name__)

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
class _AssetBase[M: None | pygame.Surface, P: None | ComputedPositionsT]:
    surface: pygame.Surface
    mask: M
    positions: P


SimpleAsset = _AssetBase[None, None]
MaskedAsset = _AssetBase[pygame.Surface, "ComputedPositionsT"]

type AssetT = SimpleAsset | MaskedAsset


class Asset[M: AssetT]:
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
        self.filename = Path(filename)
        self._loaded_asset: pygame.Surface | None = None
        self.mask = mask
        self._loaded_mask: pygame.Surface | None = None
        self._positions = positions
        self._computed_positions: ComputedPositionsT | None = None

    def __set_name__(self, owner: Assets, name: str):
        getattr(owner, "__assets_loaders__").append(self)

    @property
    def is_loaded(self):
        return self._loaded_asset is not None

    def _load_method(self, path: Path) -> pygame.Surface:
        return pygame.image.load(path)

    def load(self):
        if not self.is_loaded:
            self._loaded_asset = self._load_method(assets_dir / self.filename).convert_alpha()
            if self.mask and self._positions is not None:
                self._loaded_mask = self._load_method(
                    Path(f"{assets_dir}/{self.filename.name.split('.')[0]}_mask{self.filename.suffix}")
                )
                self._computed_positions = {
                    key: self._get_center_from_color(color) for key, color in self._positions.items()
                }
            print(f"Loaded {self.filename}")
        else:
            print(f"{self.filename} is already loaded !")

    def _get_center_from_color(self, color: tuple[int, int, int]) -> tuple[int, int]:
        if TYPE_CHECKING:
            assert self._loaded_mask is not None

        pixel_array = pygame.surfarray.pixels3d(self._loaded_mask)  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]

        # Extract the channels
        red_channel: np.ndarray[Any, Any] = pixel_array[:, :, 0]
        blue_channel: np.ndarray[Any, Any] = pixel_array[:, :, 2]
        green_channel: np.ndarray[Any, Any] = pixel_array[:, :, 1]

        # Find where all the channels match the color
        x_coords, y_coords = np.where(
            (red_channel == color[0]) & (blue_channel == color[1]) & (green_channel == color[2])
        )
        if len(x_coords) == 0 or len(y_coords) == 0:
            logger.warning("Color %s not found in the mask", color)
            return (0, 0)

        # Find the bounding box and calculate the center
        x_min, x_max = x_coords.min(), x_coords.max()
        y_min, y_max = y_coords.min(), y_coords.max()

        center_x = (x_min + x_max) // 2
        center_y = (y_min + y_max) // 2
        return (int(center_x), int(center_y))

    def __get__(self, instance: Assets | None, owner: type[Assets]) -> M:
        if not self.is_loaded:
            self.load()

        if TYPE_CHECKING:
            assert self._loaded_asset is not None

        if self.mask:
            if TYPE_CHECKING:
                assert self._loaded_mask is not None
                assert self._computed_positions is not None

            return cast(M, MaskedAsset(self._loaded_asset, self._loaded_mask, self._computed_positions))
        return cast(M, SimpleAsset(self._loaded_asset, None, None))


class SvgAsset[M: AssetT](Asset[M]):
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
        super().__init__(filename, mask, positions)  # type: ignore
        self.size = size

    def _load_method(self, path: Path) -> pygame.Surface:
        return pygame.image.load_sized_svg(path, self.size)
