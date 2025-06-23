from __future__ import annotations

from enum import Enum
from ipaddress import IPv4Address
from typing import Generic, TypeVar

from pydantic import BaseModel

from .mac_address import MacAddress

P = TypeVar("P", bound="Packet", covariant=True)  # because new syntax infer variable (wrongly)


class OsiDataModel(BaseModel):
    pass


class EthernetFrame(OsiDataModel, Generic[P]):
    destination_mac: MacAddress
    source_mac: MacAddress
    payload: P


class ARPOpCode(Enum):
    REQUEST = 1
    REPLY = 2


class Packet(OsiDataModel):
    pass


# @dataclass(kw_only=True)
class ARPPacket(Packet):
    opcode: ARPOpCode
    sender_mac: MacAddress
    sender_ip: IPv4Address
    target_mac: MacAddress | None = None  # null if request
    target_ip: IPv4Address


# @dataclass(kw_only=True)
class IPv4Packet(Packet):
    ttl: int
    source_ip: IPv4Address
    destination_ip: IPv4Address
    payload: IPv4Message


class IPv4Message(OsiDataModel):
    pass


class ICMPType(Enum):
    ECHO_REPLY = 0
    ECHO_REQUEST = 8


# @dataclass(kw_only=True)
class ICMPMessage(IPv4Message):
    type: ICMPType
    code: int = 0


class UDPDatagram(IPv4Message):
    source_port: int
    destination_port: int
    payload: UDPMessage


class UDPMessage(OsiDataModel):
    pass


class TCPSegment(IPv4Message):
    source_port: int
    destination_port: int
    payload: TCPMessage


class TCPMessage(OsiDataModel):
    pass
