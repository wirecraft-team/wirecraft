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
            new_id = await session.exec(select(Device).order_by(Device.id.desc()))
            new_id = new_id.first().id + 1

            # making sure the device has all required fields, if not add them
            if not data.type:
                raise ValueError("Device type is required")
            if not data.level_id:
                raise ValueError("Device level_id is required")
            if not data.id:
                data.id = new_id
            if not data.mac:
                data.mac = f"00:00:00:00:00:{data.id:02x}"
            if not data.ip:
                data.ip = f"192.168.1.{data.id}"
            if not data.name:
                data.name = f"{data.type} {data.id}"
            if not data.x:
                data.x = 0
            if not data.y:
                data.y = 0
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
