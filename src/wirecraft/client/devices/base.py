from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class Port:
    type: Literal["RJ45", "SFP"]  # type of the port (RJ45, SFP, ...)
    speed: int  # speed of the port (MB/s)
    PoE: bool  # does the port has PoE capabilities ?


@dataclass
class Switch:
    PoE: bool  # does the switch has PoE support ?
    capacity: int  # switching capacity in Mbps


@dataclass
class Router:
    firewall: bool  # does the router has a firewall ?
    capacity: int  # routing capacity in Mbps


@dataclass
class Host:
    ram: int  # in GB
    cpu: int  # in "score points"
    storage: int  # in GB


@dataclass
class Device:
    features: list[Host | Switch | Router]  # list of features of the device
    name: str  # name of the device
    ports: list[Port]  # list of ports
    ports_pos: list[tuple[int, int]]  # list of ports positions relative to the device sprite's center
    sprite: str  # path to the sprite of the device


@dataclass
class Service:
    type: str  # type of service (website, mail server, ...)
    name: str  # name of the service
    state: bool  # state of the service (running or not)


@dataclass
class Cable:
    type: str  # type of the cable (RJ45, SFP, ...)
    speed: int  # speed of the cable (MB/s)


first_pc = Device(
    features=[Host(ram=4, cpu=10, storage=256)],
    name="PC dla hess",
    ports=[
        Port(type="RJ45", speed=250, PoE=False),
        Port(type="RJ45", speed=1000, PoE=False),
    ],
    ports_pos=[
        (30, 0),
        (90, 0),
    ],
    sprite="PC_DEVICE",
)
