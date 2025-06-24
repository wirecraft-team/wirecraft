from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import PrivateAttr

from ..device import NetworkDevice
from ..mac_address import MacAddress
from ..osi import EthernetFrame
from ..utils import BidirectionalMap, broadcast_helper
from .base import Capability

if TYPE_CHECKING:
    from ..utils import EthernetFrameT


class BasicEthernetFrameCapability(Capability):
    handle = EthernetFrame

    def __call__(self, /, source: NetworkDevice, frame: EthernetFrameT) -> EthernetFrameT | None:
        if not frame.destination_mac.is_broadcast and frame.destination_mac != self._device.mac_address:
            self._device.log(f"Packet not for this device: {frame.destination_mac} != {self._device.mac_address}")
            return

        handler_cap = self._device.data_handlers.get(type(frame.payload))
        if not handler_cap:
            self._device.log(f"No handler found for payload type {type(frame.payload)}")
            return None

        response = handler_cap(self._device, frame.payload)
        if response is None:
            return None

        return EthernetFrame(
            destination_mac=frame.destination_mac,
            source_mac=self._device.mac_address,
            payload=response,
        )


class Layer2Switching(Capability):
    handle = EthernetFrame

    _mac_address_table: BidirectionalMap[MacAddress, int] = PrivateAttr(
        default_factory=BidirectionalMap[MacAddress, int]
    )

    def __call__(self, /, source: NetworkDevice, frame: EthernetFrameT):
        self._populate_mac_address_table(source, frame)

        if frame.destination_mac.is_broadcast:
            return self._broadcast(source, frame)

        return self._layer2_switching(source, frame)

    def _layer2_switching(self, source: NetworkDevice, frame: EthernetFrameT) -> EthernetFrameT | None:
        """Making an atomic method so a layer3 switch can reuse it."""
        if frame.destination_mac in self._mac_address_table:
            self._device.log(f"Destination MAC {frame.destination_mac} known, forwarding to device")
            device_port = self._mac_address_table[frame.destination_mac]
            return self._device.connected_devices.inverse[device_port].handle_request(self._device, frame)

        self._device.log(f"Destination MAC {frame.destination_mac} unknown, broadcasting the request")
        return self._broadcast(self._device, frame)

    def _populate_mac_address_table(self, source: NetworkDevice, frame: EthernetFrameT):
        """
        Populate the MAC address table with the source MAC address and the port it was received on.
        This is used to learn the MAC addresses of connected devices.
        """
        if frame.source_mac not in self._mac_address_table:
            self._device.log(
                f"Adding {frame.source_mac} to MAC address table on interface {self._device.connected_devices[source]}"
            )
            self._mac_address_table[frame.source_mac] = self._device.connected_devices[source]

    def _broadcast(self, source: NetworkDevice, frame: EthernetFrameT):
        self._device.log(f"Broadcast packet received from {frame.source_mac}, forwarding to all other devices")
        for device in broadcast_helper(self._device.connected_devices, source):
            response = device.handle_request(self._device, frame)
            if response:
                self._device.log(f"Got a response from {device}!")
                self._device.log("Updating MAC address table.")
                self._mac_address_table[response.source_mac] = self._device.connected_devices[device]
                self._device.log("Return response to source.")
                return response
