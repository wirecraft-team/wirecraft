from __future__ import annotations

from ipaddress import IPv4Address, IPv4Network
from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import select

from ..database import Cable, Device, async_session
from ..handlers_core import Handler, event
from ..networking.capabilities import ARPCapability, ICMPCapability, IPv4Capability, Layer2Switching, Routing
from ..networking.device import NetworkDevice
from ..static import levels

if TYPE_CHECKING:
    from ..static.base import Level


class LaunchData(BaseModel):
    level_id: int


class LaunchHandler(Handler):
    @event
    async def launch_simulation(self, data: LaunchData):
        level = levels[data.level_id]
        await self.build_network(level)

    async def build_network(self, level: Level):
        async with async_session() as session:
            stmt = select(Device).where(Device.level_id == level.id)
            result = await session.exec(stmt)
            devices = result.all()

            stmt = select(Cable).where(Cable.level_id == level.id)
            result = await session.exec(stmt)
            cables = result.all()

        device_map: dict[int, NetworkDevice] = {}

        for device in devices:
            network_device = NetworkDevice(mac_address=device.mac)
            device_map[device.id] = network_device

            if device.ip:
                network_device.add_capability(IPv4Capability(ip_address=IPv4Address(device.ip)))

            if device.type == "switch":
                network_device.add_capability(Layer2Switching())
            if device.type == "pc":
                routing = Routing()
                routing.routing_table.add_route(IPv4Network("192.168.0.0/24"), interface=0)
                network_device.add_capability(routing)
                network_device.add_capability(ICMPCapability())
                network_device.add_capability(ARPCapability())

        for cable in cables:
            device_a = device_map[cable.device_id_1]
            device_b = device_map[cable.device_id_2]

            device_a.add_connection(cable.port_1, device_b, cable.port_2)
