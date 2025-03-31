from __future__ import annotations

from collections.abc import Sequence

from pydantic import BaseModel
from sqlmodel import select

from ..database.base import device_dict
from ..database.models import Device, async_session
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


class DevicesHandler(Handler):
    @event
    async def get_level_devices(self, data: GetLevelDevicesData) -> Sequence[Device]:
        statement = select(Device).where(Device.level_id == data.level_id)
        async with async_session() as session:
            result = await session.exec(statement)
            devices = result.all()
        return devices

    @event
    async def add_device(self, data: Device):
        async with async_session() as session:
            session.add(data)
            await session.commit()

    @event
    async def get_device_props(self, data: GetDevicePropsData):
        async with async_session() as session:
            statement = select(Device.name).where(Device.id == data.device_id)
            result = await session.exec(statement)
            device_name = result.one()
            return device_dict[device_name]

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
