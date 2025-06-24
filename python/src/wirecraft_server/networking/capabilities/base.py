from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel

from ..device import NetworkDevice
from ..osi import OsiDataModel


class Capability(BaseModel):
    handle: ClassVar[type[OsiDataModel] | None] = None

    def bind_to(self, device: NetworkDevice):
        self._device = device

    def __call__(self, /, source: NetworkDevice, data: Any) -> Any | None:
        """
        Call the capability with the data.
        This method should be overridden in subclasses to handle specific data types.
        """
        raise NotImplementedError("This method should be overridden in subclasses")
