from __future__ import annotations

import igraph as ig
from pydantic import BaseModel, Field
from sqlmodel import select

from ._logger import logging
from .database.models import Cable, Device, async_session

logger = logging.getLogger(__name__)


class DevicesManager:
    def __init__(self):
        self._devices: list[NetworkDevice] = []
        self._map_id_to_index: dict[int, int] = {}
        # self._map_index_to_id: dict[int, int] = {}  # Reverse mapping for convenience

    def __len__(self) -> int:
        return len(self._devices)

    def __repr__(self):
        return f"DevicesManager({len(self._devices)} devices)"

    def __iter__(self):
        """
        Iterate over the devices in the manager.
        """
        return iter(self._devices)

    def clear(self):
        self._devices.clear()
        self._map_id_to_index.clear()
        # self._map_index_to_id.clear()

    def add_device(self, device: NetworkDevice):
        if device.id in self._map_id_to_index:
            raise ValueError(f"Device with ID {device.id} already exists.")
        self._devices.append(device)
        self._map_id_to_index[device.id] = len(self._devices) - 1
        # self._map_index_to_id[len(self._devices) - 1] = device.id

    def get_graph_index(self, device_id: int) -> int:
        return self._map_id_to_index[device_id]

    def get_device_by_graph_index(self, graph_index: int) -> NetworkDevice:
        """
        Get a device by its graph index
        """
        return self._devices[graph_index]

    def get_device_by_id(self, device_id: int) -> NetworkDevice:
        """
        Get a device by its ID
        """
        return self.get_device_by_graph_index(self.get_graph_index(device_id))


# Use a global variable because we need to have things working quickly, it's "temporary"
device_manager = DevicesManager()


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
                path = graph.get_shortest_path(
                    device_manager.get_graph_index(self.id),
                    to=device_manager.get_graph_index(device.id),
                    output="vpath",
                )
                if path:
                    # return already existing device node object of the first device in the path (next hop)
                    self.table[device.ip] = device_manager.get_device_by_graph_index(path[1])
            return True

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
        device_manager.clear()
        for device in result.all():
            if device.ip is None:
                continue
            device_manager.add_device(NetworkDevice(id=device.id, type=device.type, ip=device.ip))
        logger.debug("Devices updated: %s", device_manager)


async def update_routing_tables():
    graph = await update_network_graph()
    for device in device_manager:
        await device.create_routing_table(graph)


async def update_network_graph():
    async with async_session() as session:
        cables = await session.exec(select(Cable.device_id_1, Cable.device_id_2))
        cables = [tuple[int, int](map(device_manager.get_graph_index, cable)) for cable in cables.all()]
        nb_vertices = len(device_manager)

        return ig.Graph(nb_vertices, cables)
