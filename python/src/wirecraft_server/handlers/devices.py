from __future__ import annotations

from collections.abc import Sequence
from ipaddress import IPv4Address

from pydantic import BaseModel, Field
from sqlmodel import select

from ..database import Device, async_session
from ..handlers_core import Handler, event


class GetLevelDevicesData(BaseModel):
    """
    Payload for the get_level_devices event.
    """

    level_id: int


class GetDevicePropsData(BaseModel):
    """
    Payload for the get_device_props ws method.
    """

    device_id: int


class UpdateDevicePositionData(BaseModel):
    """
    Payload for the update_device_position ws method.
    """

    device_id: int
    x: int
    y: int


class UpdateDeviceData(BaseModel):
    """
    Payload for the update_device_ip ws method.
    TODO(airopi): this could be merged with UpdateDevicePositionData
    """

    device_id: int
    ip: IPv4Address | None = Field(default=None)
    name: str | None = Field(default=None)


class GetDeviceData(BaseModel):
    """
    Payload for the get_device ws method.
    """

    device_id: int


class DevicesHandler(Handler):
    @event
    async def get_level_devices(self, data: GetLevelDevicesData) -> Sequence[Device]:
        async with async_session() as session:
            statement = select(Device).where(Device.level_id == data.level_id)
            result = await session.exec(statement)
            devices = result.all()
        return devices

    @event
    async def get_device(self, data: GetDeviceData) -> Device:
        async with async_session() as session:
            statement = select(Device).where(Device.id == data.device_id)
            result = await session.exec(statement)
            device = result.one()
        return device

    @event
    async def add_device(self, data: Device):
        async with async_session() as session:
            session.add(data)
            await session.commit()

    @event
    async def update_device_position(self, data: UpdateDevicePositionData):
        async with async_session() as session:
            statement = select(Device).where(Device.id == data.device_id)
            result = await session.exec(statement)
            device = result.one()
            device.x = data.x
            device.y = data.y
            await session.commit()
        return device

    @event
    async def update_device(self, data: UpdateDeviceData) -> Device:
        async with async_session() as session:
            stmt = select(Device).where(Device.id == data.device_id)
            result = await session.exec(stmt)
            device = result.one()
            if data.name:
                device.name = data.name
            if data.ip is not None:
                device.ip = str(data.ip)
            else:
                device.ip = None
            await session.commit()
        return device
