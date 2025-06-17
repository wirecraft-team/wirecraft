from __future__ import annotations

import igraph as ig
from pydantic import BaseModel, Field
from sqlmodel import select

from ._logger import logging
from .database.models import Cable, Device, async_session

logger = logging.getLogger(__name__)
global_device_list: list[NetworkDevice] = []


class Packet(BaseModel):
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


class NetworkDevice(BaseModel):
    """
    A node in the network graph
    """

    type: str
    id: int
    ip: str
    table: dict[str, NetworkDevice] = Field(default_factory=dict)

    def __hash__(self) -> int:
        return hash(self.id)

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
                if device.ip is None:
                    # No IP address assigned to the device, skip it
                    continue
                # Get the shortest path to each device
                path = graph.get_shortest_path(self.id - 1, to=device.id - 1, output="vpath")
                if path:
                    # return already existing device node object of the first device in the path (next hop)
                    self.table[device.ip] = self.get_device_by_id(path[1])
            return True

    def get_device_by_id(self, device_id: int) -> NetworkDevice:
        """
        Get a device by its ID
        """
        for device in global_device_list:
            if device.id == device_id + 1:
                return device
        raise ValueError(f"Device {device_id} not found in neighbors ({[dev.id for dev in global_device_list]})")

    def process_packet(self, packet: Packet) -> bool:
        """
        Process a packet
        """
        logger.debug("Device %s processing packet: %s", self.id, packet)
        match self.type:
            case "switch":
                return self.process_packet_switch(packet)
            case "router":
                return self.process_packet_router(packet)
            case "pc":
                return self.process_packet_host(packet)
            case _:
                logger.debug("Unknown device type: %s", self.type)
                return False

    def process_packet_switch(self, packet: Packet) -> bool:
        if packet.dst_ip_adress == self.ip:
            logger.debug("Packet received by %s: %s", self.id, packet)
            return True
        if packet.ttl <= 0:
            logger.debug("Packet TTL expired: %s", packet)
            return False
        return any(value.process_packet(packet) for value in set(self.table.values()) if value.id != packet.src_id)

    def process_packet_router(self, packet: Packet) -> bool:
        if packet.dst_ip_adress == self.ip:
            logger.debug("Packet received by %s: %s", self.id, packet)
            return True
        if packet.ttl <= 0:
            logger.debug("Packet TTL expired: %s", packet)
            return False
        packet.ttl_decrement()
        return any(value.process_packet(packet) for value in set(self.table.values()) if value.id != packet.src_id)

    def process_packet_host(self, packet: Packet) -> bool:
        if packet.dst_ip_adress == self.ip:
            logger.debug("Packet received by %s: %s", self.id, packet)
            return True
        if packet.ttl <= 0:
            logger.debug("Packet TTL expired: %s", packet)
            return False
        return False

    def ping(self, dst_ip: str) -> bool:
        """
        Ping a device
        """
        if dst_ip == self.ip:
            logger.debug("Ping received by %s", self.id)
            return True
        try:
            # self.table[dst_ip] is the next hop to the destination
            return self.table[dst_ip].process_packet(
                Packet(
                    src_ip_adress=self.ip,
                    dst_ip_adress=dst_ip,
                    src_id=self.id,
                    dst_id=self.table[dst_ip].id,
                    message="ping",
                )
            )
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
        global_device_list.clear()
        global_device_list.extend(
            NetworkDevice(id=device.id, type=device.type, ip=device.ip)
            for device in result.all()
            if device.ip is not None
        )
        logger.debug("Devices updated: %s", global_device_list)


async def update_routing_tables():
    graph = await update_network_graph()
    for device in global_device_list:
        await device.create_routing_table(graph)


async def update_network_graph():
    async with async_session() as session:
        devices = await session.exec(select(Device.id))
        devices = list(devices.all())
        cables = await session.exec(select(Cable.device_id_1, Cable.device_id_2))
        cables = list(cables.all())
        nb_vertices = len(devices)

        print(devices, cables)
        return ig.Graph(nb_vertices, cables)
