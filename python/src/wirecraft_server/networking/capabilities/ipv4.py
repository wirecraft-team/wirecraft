from __future__ import annotations

from ipaddress import IPv4Address

from ..device import NetworkDevice
from ..osi import IPv4Packet
from .base import Capability


class IPv4Capability(Capability):
    handle = IPv4Packet

    ip_address: IPv4Address

    def __call__(self, source: NetworkDevice, packet: IPv4Packet) -> IPv4Packet | None:
        ipv4_cap = self._device.get_capability(IPv4Capability)
        if ipv4_cap is None:
            self._device.log("IPv4 capability not found, cannot handle ARP request.")
            return None

        if packet.destination_ip != ipv4_cap.ip_address:
            self._device.log(f"Packet not for this device: {packet.destination_ip} != {ipv4_cap.ip_address}")
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
            source_ip=ipv4_cap.ip_address,
            destination_ip=packet.source_ip,  # Reply to the source IP
            payload=response,
        )
