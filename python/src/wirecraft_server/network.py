from __future__ import annotations

from dataclasses import dataclass

import igraph as ig
from pydantic import BaseModel
from sqlmodel import select
import matplotlib.pyplot as plt


from ._logger import logging
from .database.models import Cable, Device, async_session

logger = logging.getLogger(__name__)
devices: list[NetworkDevice] = []


@dataclass
class Packet:
    src_ip_adress: str
    dst_ip_adress: str
    src_id: int  # mimics the MAC address
    dst_id: int  # mimics the MAC address
    message: str
    ttl: int = 64

    def ttl_decrement(self):
        """
        Decrease the TTL of the packet
        """
        self.ttl -= 1
        if self.ttl <= 0:
            logger.debug("Packet TTL expired: %s", self)
            return False
        return True


class NetworkDevice:
    """
    A node in the network graph
    """

    def __init__(self, device_id: int, type: str, ip: str):
        self.type = type
        self.id = device_id
        self.ip = ip
        self.neighbors: list[NetworkDevice] = []
        self.table: dict[str, NetworkDevice] = {}

    async def create_routing_table(self, graph: ig.Graph):
        """
        Create a routing table for the node
        """
        async with async_session() as session:
            # Get all devices in the network
            statement = select(Device).where(Device.id != self.id)
            result = await session.exec(statement)
            devices = result.all()
            for device in devices:
                # Get the shortest path to each device
                path = graph.get_shortest_path(self.id - 1, to=device.id - 1, output="vpath")
                if path:
                    # return already existing device node object of the first device in the path
                    self.table[device.ip] = self.get_device_by_id(path[1])
            return True

    def get_device_by_id(self, device_id: int) -> NetworkDevice:
        """
        Get a device by its ID
        """
        for device in devices:
            if device.id == device_id + 1:
                return device
        raise ValueError(f"Device {device_id} not found in neighbors ({[dev.id for dev in devices]})")

    def process_packet(self, packet: Packet) -> bool:
        """
        Process a packet
        """
        logger.debug("Deivce %s processing packet: %s", self.id, packet)
        match self.type:
            case "switch":
                return self.process_switch(packet)
            case "router":
                return self.process_router(packet)
            case "pc":
                return self.process_host(packet)
            case _:
                logger.debug("Unknown device type: %s", self.type)
                return False

    def process_switch(self, packet: Packet) -> bool:
        if packet.dst_ip_adress == self.ip:
            logger.debug("Packet received by %s: %s", self.id, packet)
            return True
        if packet.ttl <= 0:
            logger.debug("Packet TTL expired: %s", packet)
            return False
        return any(neighbor.process_packet(packet) for neighbor in self.neighbors)

    def process_router(self, packet: Packet) -> bool:
        if packet.dst_ip_adress == self.ip:
            logger.debug("Packet received by %s: %s", self.id, packet)
            return True
        if packet.ttl <= 0:
            logger.debug("Packet TTL expired: %s", packet)
            return False
        packet.ttl_decrement()
        return any(neighbor.process_packet(packet) for neighbor in self.neighbors)

    def process_host(self, packet: Packet) -> bool:
        if packet.dst_ip_adress == self.ip:
            logger.debug("Packet received by %s: %s", self.id, packet)
            return True
        if packet.ttl <= 0:
            logger.debug("Packet TTL expired: %s", packet)
            return False
        return False

    def is_neighbour(self, dst_id: int) -> int:
        for device in self.neighbors:
            if device.id == dst_id:
                return device.id
        return -1

    def ping(self, dst_ip: str) -> bool:
        """
        Ping a device
        """
        if dst_ip == self.ip:
            logger.debug("Ping received by %s", self.id)
            return True
        try:
            return self.table[dst_ip].process_packet(Packet(self.ip, dst_ip, self.id, self.table[dst_ip].id, "ping"))
        except KeyError:
            logger.debug("Device %s not found in routing table", dst_ip)
            return False


async def update_devices():
    """
    Update the devices in the network
    """
    async with async_session() as session:
        statement = select(Device)
        result = await session.exec(statement)
        devices.clear()
        devices.extend(NetworkDevice(device_id=device.id, type=device.type, ip=device.ip) for device in result.all())
        logger.debug("Devices updated: %s", devices)


async def update_routing_tables():
    graph = await update_network_graph()
    for device in devices:
        await device.create_routing_table(graph)


async def update_network_graph():
    async with async_session() as session:
        devices = await session.exec(select(Device.id))
        devices = list(devices.all())
        cables = await session.exec(select(Cable.device_id_1 - 1, Cable.device_id_2 - 1))
        cables = list(cables.all())
        nb_vertices = len(devices)
        return ig.Graph(nb_vertices, cables)


async def get_device_by_id(device_id: int) -> Device | None:
    """
    Get a device by its ID
    """
    async with async_session() as session:
        statement = select(Device).where(Device.id == device_id)
        result = await session.exec(statement)
        device = result.first()
        if device is None:
            logger.debug("Device %s not found", device_id)
            return None
        return device
