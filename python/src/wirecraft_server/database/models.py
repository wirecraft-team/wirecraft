from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel

from ..networking.mac_address import MacAddress
from ..utils import id_to_mac


class Cable(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    device_id_1: int = Field(default=None, foreign_key="device.id")
    port_1: int
    device_id_2: int = Field(default=None, foreign_key="device.id")
    port_2: int
    level_id: int = Field(default=None, foreign_key="levelstate.id")


class Device(SQLModel, table=True):
    """
    id: managed by the database
    name: name of the device
    type: type of the device, e.g. "switch", "pc"
    x: x coordinate in the level
    y: y coordinate in the level
    # frozen: the device can be moved, but not configured or deleted
    frozen_name: the device cannot be renamed, useful for tasks that require a specific device to be present
    deletable: to set a device as non-deleted, useful for tasks that require a specific device to be present
    fixed_ref: reference to a pre-defined device, useful for tasks that require a specific device to be present
    level_id: the level this device belongs to, used to group devices in a level
    ip: the IP address of the device, can be None if not assigned
    """

    id: int = Field(default=None, primary_key=True)
    name: str
    type: str
    x: int
    y: int
    # frozen: bool = Field(default=False, exclude=True)
    frozen_name: bool = Field(default=False, exclude=True)
    deletable: bool = Field(default=True, exclude=True)
    level_id: int = Field(default=None, foreign_key="levelstate.id")
    ip: str | None = None
    # default_gateway: str | None = None
    # subnet_mask: str | None = None

    __table_args__ = (UniqueConstraint("name", "level_id", name="uq_device_name_level_id"),)

    @property
    def mac(self) -> MacAddress:
        return id_to_mac(self.id)


class LevelState(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    completed: bool = False


# async def init():
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.drop_all)
#         await conn.run_sync(SQLModel.metadata.create_all)

#     level_dev = LevelState(completed=False)
#     # Add level first to get an ID before assigning it to devices
#     async with async_session() as session:
#         if not (await session.exec(select(LevelState))).first():
#             session.add(level_dev)
#             await session.commit()
#             await session.refresh(level_dev)
#             if TYPE_CHECKING:
#                 assert isinstance(level_dev.id, int)
#             switch1 = Device(name="sw1", type="switch", x=0, y=0, level_id=level_dev.id, ip="192.168.1.1")
#             pc1 = Device(
#                 name="pc1",
#                 type="pc",
#                 x=400,
#                 y=-400,
#                 level_id=level_dev.id,
#                 ip="192.168.1.2",
#                 default_gateway=switch1.ip,
#             )
#             pc2 = Device(
#                 name="pc2",
#                 type="pc",
#                 x=-400,
#                 y=-400,
#                 level_id=level_dev.id,
#                 ip="192.168.1.3",
#                 default_gateway=switch1.ip,
#             )
#             session.add(switch1)
#             session.add(pc1)
#             session.add(pc2)
#             await session.commit()
#             # cable = Cable(device_id_1=switch1.id, port_1=1, device_id_2=pc1.id, port_2=1, level_id=level_dev.id)
#             # session.add(cable)
#             await session.commit()
#     # if there are cables with devices id that are < 0 then delete them as they were in a placing state when the game closed
#     async with async_session() as session:
#         cables = (await session.exec(select(Cable))).all()
#         for cable in cables:
#             if cable.device_id_1 < 0:
#                 await session.delete(cable)
#         await session.commit()
