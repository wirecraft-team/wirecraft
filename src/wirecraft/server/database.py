from __future__ import annotations


class Port:
    type: str  # type of the port (RJ45, SFP, ...)
    speed: int  # speed of the port (MB/s)
    state: bool  # state of the port (up or not)


class Switch:
    pass


class Router:
    pass


class Host:
    def __init__(self, ram: int, cpu: int, storage: int):
        self.ram = ram  # ram size (GB)
        self.cpu = cpu  # cpu score (points)
        self.storage = storage  # storage size (GB)


class Device:
    id: int  # id of the device
    features: list[Host | Switch | Router]  # list of features of the device
    name: str  # name of the device
    ports: list[Port]  # list of ports type
    state: bool  # state of the device (running or not)


class Service:
    type: str  # type of service (website, mail server, ...)
    name: str  # name of the service
    port: int  # port of the service
    protocol: str  # protocol of the service
    host_id: int  # id of the host where the service is running
    state: bool  # state of the service (running or not)


class Cable:
    type: str  # type of the cable (RJ45, SFP, ...)
    speed: int  # speed of the cable (MB/s)
