from __future__ import annotations

from typing import Annotated

from pydantic import RootModel
from pydantic_extra_types.mac_address import MacAddress as MacAddressPydantic


class MacAddress(RootModel[str]):
    root: Annotated[str, MacAddressPydantic]

    @classmethod
    def broadcast(cls) -> MacAddress:
        """
        Create a MacAddress instance representing the broadcast address.
        """
        return cls("ff:ff:ff:ff:ff:ff")

    @property
    def is_broadcast(self) -> bool:
        """
        Check if the MAC address is a broadcast address.
        A broadcast MAC address is ff:ff:ff:ff:ff:ff.
        """
        return self == MacAddress("ff:ff:ff:ff:ff:ff")

    def __hash__(self):
        return hash(self.root)

    def __repr__(self):
        return self.root

    __str__ = __repr__
