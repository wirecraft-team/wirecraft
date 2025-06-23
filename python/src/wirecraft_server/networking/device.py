from __future__ import annotations

from ipaddress import IPv4Address
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from .mac_address import MacAddress
from .osi import OsiDataModel
from .utils import BidirectionalMap

if TYPE_CHECKING:
    from .utils import EthernetFrameT


class NetworkDevice(BaseModel):
    mac_address: MacAddress  # mac_address should be private, but we need to initialize it in the constructor, and Pydantic does not allow private fields to be set in the constructor
    # Map a device to a port
    connected_devices: BidirectionalMap[NetworkDevice, int] = Field(
        init=False, default_factory=BidirectionalMap["NetworkDevice", int]
    )
    data_handlers: dict[type[OsiDataModel], Capability] = Field(
        init=False, default_factory=dict[type[OsiDataModel], "Capability"]
    )
    capabilities: dict[type[Capability], Capability] = Field(
        init=False, default_factory=dict[type["Capability"], "Capability"]
    )

    def add_connection(self, port: int, device: NetworkDevice, other_device_port: int):
        """Add a connection to another device on a specific port."""
        self.log(f"Adding connection from {self} on port {port} to {device} on port {other_device_port}")
        self.connected_devices.set(device, port)
        device.connected_devices.set(self, other_device_port)

    def add_capability(self, *capabilities: Capability):
        for capability in capabilities:
            if not isinstance(self, capability.device_type):
                raise TypeError(f"Capability {capability} is not compatible with device type {self.__class__.__name__}")
            capability.bind_to(self)
            if capability.handle:
                self.data_handlers[capability.handle] = capability
            self.capabilities[type(capability)] = capability

    def get_capability[C: Capability](self, capability_type: type[C]) -> C | None:
        return self.capabilities.get(capability_type, None)  # type: ignore

    def __repr__(self):
        return f"{self.__class__.__name__}({self.mac_address})"

    __str__ = __repr__

    def handle_request(self, source: NetworkDevice, frame: EthernetFrameT) -> EthernetFrameT | None:
        """
        In our model, we don't send requests through "cables".
        Instead, we get the NetworkDevice object 'connected' to a port, and this method, "handle_request", simulates
        the behavior of the device when it receives a packet.
        This method should be overridden in subclasses to handle specific packet types.
        """
        self.log(f"Handling request from {source}")

        cap = self.data_handlers.get(type(frame))
        if not cap:
            self.log(f"No handler found for frame type {type(frame)}")
            return None

        return cap(source, frame)

    def __hash__(self):
        return hash(self.mac_address)

    def __eq__(self, value: object) -> bool:
        """To compare 2 devices, we compare their MAC addresses. Two different devices with the same MAC address SHOULD NOT exist."""
        if not isinstance(value, NetworkDevice):
            return False
        return self.mac_address == value.mac_address

    def log(self, message: str):
        """Log a message from the device."""
        if hasattr(self, "ip_address"):
            message = f"[{self.__class__.__name__}] {self.mac_address} ~ {getattr(self, 'ip_address')} : {message}"
        else:
            message = f"[{self.__class__.__name__}] {self.mac_address} : {message}"
        print(message)


class IPNetworkDevice(NetworkDevice):
    ip_address: IPv4Address


from .capabilities.base import Capability  # noqa: E402 avoid circular import

IPNetworkDevice.model_rebuild()
BidirectionalMap["NetworkDevice", int].model_rebuild()
