from dataclasses import dataclass

from sqlmodel import or_, select

from .database.models import Cable, Device, async_session


@dataclass
class Packet:
    src_ip: str
    dst_ip: str
    src_mac: str
    dst_mac: str
    message: str


async def ping(src_device_id: int, dest_device_ip: str):
    """
    Simulate a ping command between two devices
    """
    # Get the source device's MAC and IP address
    for cable in await get_cables_from_device_id(src_device_id):
        next_hop_id = cable.device_id_2 if cable.device_id_1 == src_device_id else cable.device_id_1
        next_hop = await get_device_by_id(next_hop_id)
        if next_hop is None:
            return 0
        if next_hop.ip == dest_device_ip:
            return 1
        elif next_hop.type == "switch":
            await ping(next_hop_id, dest_device_ip)
        else:
            return 0
    return 0


async def get_cables_from_device_id(device_id: int):
    """
    Get all cables connected to a device
    """
    async with async_session() as session:
        statement = select(Cable).where(or_(Cable.device_id_1 == device_id, Cable.device_id_2 == device_id))
        result = await session.exec(statement)
        cables = result.all()
    return list(cables)


async def get_device_by_id(device_id: int):
    """
    Get a device by its ID
    """
    async with async_session() as session:
        statement = select(Device).where(Device.id == device_id)
        result = await session.exec(statement)
        device = result.first()
    return device
