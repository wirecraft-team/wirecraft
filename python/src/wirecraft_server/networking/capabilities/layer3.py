# TODO(airopi): this is old code that should be rewrite to adopt the new modular design

# from __future__ import annotations

# from ipaddress import IPv4Address, IPv4Network
# from typing import TYPE_CHECKING, Any, ClassVar, Protocol, TypeVar

# from pydantic import PrivateAttr

# from ..mac_address import MacAddress
# from ..osi import ARPOpCode, ARPPacket, EthernetFrame, ICMPMessage, ICMPType, IPv4Packet, Packet
# from ..routing import Route, RoutingTable
# from ..utils import BidirectionalMap
# from .base import ARPCapability, IPNetworkDevice, NetworkDevice, Routing
# from .layer2 import Layer2Switch

# if TYPE_CHECKING:
#     from ..utils import EthernetFrameT


# P = TypeVar("P", bound=Packet, contravariant=True, default=Packet)
# D = TypeVar("D", bound=NetworkDevice, contravariant=True, default=NetworkDevice)


# class PacketHandler(Protocol[D, P]):
#     def __call__(_self, self: D, source: NetworkDevice, packet: P) -> Packet | None: ...


# class Layer3Device(NetworkDevice):
#     ip_address: IPv4Address  # ip_address should be private, but we need to initialize it in the constructor, and Pydantic does not allow private fields to be set in the constructor

#     def handle_request(self, source: NetworkDevice, frame: EthernetFrame[Packet]) -> EthernetFrame[Packet] | None:
#         self.log(f"Handling request from {source}")

#         if not frame.destination_mac.is_broadcast and frame.destination_mac != self.mac_address:
#             self.log(f"Packet not for this device: {frame.destination_mac} != {self.mac_address}")
#             return

#         for packet_type, handler in self._packet_handlers.items():
#             if isinstance(frame.payload, packet_type):
#                 response_payload = handler(self, source, frame.payload)
#                 if response_payload is not None:
#                     return EthernetFrame(
#                         destination_mac=frame.destination_mac,
#                         source_mac=self.mac_address,
#                         payload=response_payload,
#                     )
#         else:
#             self.log(f"Unsupported packet type: {type(frame.payload)}")


# class Layer3Switch(Layer3Device, Layer2Switch):
#     def handle_request(self, source: NetworkDevice, frame: EthernetFrameT) -> EthernetFrameT | None:
#         self.log(f"Handling request from {source.mac_address}")
#         self._populate_mac_address_table(source, frame)

#         response = super().handle_request(source, frame)
#         if response is not None:
#             return response

#         if frame.destination_mac.is_broadcast:
#             return self._broadcast(source, frame)

#         if frame.destination_mac != self.mac_address:
#             self.log("Packet not for this device, doing Layer 2 forwarding.")
#             return self._layer2_switching(source, frame)


# class Computer(Layer3Device):
#     def model_post_init(self, __context: Any):
#         super().model_post_init(__context)
#         self._routing_table.add_route(IPv4Network("192.168.0.0/24"))


# class Router(Layer3Device):
#     pass
