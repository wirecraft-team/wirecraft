from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import PrivateAttr

from ..device import IPNetworkDevice, NetworkDevice
from ..osi import IPv4Packet
from .base import Capability


class IPv4Capability(Capability):
    handle = IPv4Packet
    device_type = IPNetworkDevice
    if TYPE_CHECKING:
        _device: IPNetworkDevice = PrivateAttr()  # type: ignore

    def __call__(self, source: NetworkDevice, packet: IPv4Packet) -> IPv4Packet | None:
        if packet.destination_ip != self._device.ip_address:
            self._device.log(f"Packet not for this device: {packet.destination_ip} != {self._device.ip_address}")
            return None

        handler_cap = self._device.data_handlers.get(type(packet.payload))
        if not handler_cap:
            self._device.log(f"No handler found for payload type {type(packet.payload)}")
            return None

        response = handler_cap(self._device, packet.payload)
        if response is None:
            return None

        return IPv4Packet(
            ttl=packet.ttl,  # TTL should be decremented in a real implementation
            source_ip=self._device.ip_address,
            destination_ip=packet.source_ip,  # Reply to the source IP
            payload=response,
        )
