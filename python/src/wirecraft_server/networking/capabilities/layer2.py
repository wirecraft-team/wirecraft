# TODO(airopi): this is old code that should be rewrite to adopt the new modular design

# from __future__ import annotations

# from typing import TYPE_CHECKING

# from pydantic import PrivateAttr

# from ..mac_address import MacAddress
# from ..utils import BidirectionalMap, broadcast_helper
# from .base import NetworkDevice

# if TYPE_CHECKING:
#     from ..utils import EthernetFrameT


# class Layer2Switch(NetworkDevice):
#     _mac_address_table: BidirectionalMap[MacAddress, int] = PrivateAttr(
#         default_factory=BidirectionalMap[MacAddress, int]
#     )

#     def handle_request(self, source: NetworkDevice, frame: EthernetFrameT):
#         self.log(f"Handling request from {source.mac_address}")

#         self._populate_mac_address_table(source, frame)

#         if frame.destination_mac.is_broadcast:
#             return self._broadcast(source, frame)

#         return self._layer2_switching(source, frame)

#     def _layer2_switching(self, source: NetworkDevice, frame: EthernetFrameT) -> EthernetFrameT | None:
#         """Making an atomic method so a layer3 switch can reuse it."""
#         if frame.destination_mac in self._mac_address_table:
#             self.log(f"Destination MAC {frame.destination_mac} known, forwarding to device")
#             device_port = self._mac_address_table[frame.destination_mac]
#             return self.connected_devices.inverse[device_port].handle_request(source, frame)

#         self.log(f"Destination MAC {frame.destination_mac} unknown, broadcasting the request")
#         return self._broadcast(source, frame)

#     def _populate_mac_address_table(self, source: NetworkDevice, frame: EthernetFrameT):
#         """
#         Populate the MAC address table with the source MAC address and the port it was received on.
#         This is used to learn the MAC addresses of connected devices.
#         """
#         if frame.source_mac not in self._mac_address_table:
#             self.log(f"Adding {frame.source_mac} to MAC address table")
#             self._mac_address_table[frame.source_mac] = self.connected_devices[source]

#     def _broadcast(self, source: NetworkDevice, frame: EthernetFrameT):
#         self.log(f"Broadcast packet received from {frame.source_mac}, forwarding to all other devices")
#         for device in broadcast_helper(self.connected_devices, source):
#             response = device.handle_request(source, frame)
#             if response:
#                 self.log(f"Got a response from {device}!")
#                 self.log("Updating MAC address table.")
#                 self._mac_address_table[response.source_mac] = self.connected_devices[device]
#                 self.log("Return response to source.")
#                 return response
