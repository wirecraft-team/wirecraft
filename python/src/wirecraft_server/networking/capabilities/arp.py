from __future__ import annotations

from ipaddress import IPv4Address

from pydantic import Field

from ..device import NetworkDevice
from ..mac_address import MacAddress
from ..osi import ARPOpCode, ARPPacket
from ..utils import BidirectionalMap
from .base import Capability
from .ipv4 import IPv4Capability


class ARPCapability(Capability):
    handle = ARPPacket

    arp_table: BidirectionalMap[IPv4Address, MacAddress] = Field(
        init=False, default_factory=BidirectionalMap[IPv4Address, MacAddress]
    )

    def __call__(self, /, source: NetworkDevice, packet: ARPPacket) -> ARPPacket | None:
        ipv4_cap = self._device.get_capability(IPv4Capability)
        if ipv4_cap is None:
            self._device.log("IPv4 capability not found, cannot handle ARP request.")
            return None

        self._device.log(f"Handling ARP request from {source}")
        self._device.log(f"Adding {packet.sender_ip} to ARP table with MAC {packet.sender_mac}")
        self.arp_table[packet.sender_ip] = packet.sender_mac

        if packet.target_ip != ipv4_cap.ip_address:
            self._device.log(f"ARP request for {packet.target_ip}, not for this device.")
            return

        self._device.log(f"ARP request for {ipv4_cap.ip_address} (self), replying with MAC {self._device.mac_address}")
        return ARPPacket(
            opcode=ARPOpCode.REPLY,
            sender_mac=self._device.mac_address,
            sender_ip=ipv4_cap.ip_address,
            target_mac=packet.sender_mac,
            target_ip=packet.sender_ip,
        )

    def resolve_mac(self, target_ip: IPv4Address) -> MacAddress | None:
        self._device.log(f"Resolving MAC for {target_ip}")
        if target_ip in self.arp_table:
            self._device.log(f"Found MAC {self.arp_table.get(target_ip)} in arp table for IP {target_ip}")
            return self.arp_table.get(target_ip)

        self._device.log(f"IP {target_ip} not in ARP table")

        from ..requests import send_arp_request

        send_arp_request(self._device, target_ip)
        mac_address = self.arp_table.get(target_ip)
        if mac_address is None:
            self._device.log(f"Failed to resolve MAC address for {target_ip}")
        return mac_address
