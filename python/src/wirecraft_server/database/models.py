from typing import TYPE_CHECKING

from sqlmodel import (
    Field,  # type: ignore
    Session,
    SQLModel,
    create_engine,
    select,
)

db = "sqlite:///database.db"
engine = create_engine(db)


class Cable(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    id_device_1: int = Field(default=None, foreign_key="device.id")
    port_1: int
    id_device_2: int = Field(default=None, foreign_key="device.id")
    port_2: int
    id_level: int = Field(default=None, foreign_key="level.id")


class Device(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    type: str
    x: int
    y: int
    id_level: int = Field(default=None, foreign_key="level.id")


class Level(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    completed: bool = False


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_level: int = Field(default=None, foreign_key="level.id")
    name: str
    completed: bool = False


def init():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    level_dev = Level(completed=False)
    # Add level first to get an ID before assigning it to devices
    with Session(engine) as session:
        if not session.exec(select(Level)).first():
            session.add(level_dev)
            session.commit()
            session.refresh(level_dev)
            if TYPE_CHECKING:
                assert isinstance(level_dev.id, int)
            switch1 = Device(name="Switch 1", type="switch", x=0, y=0, id_level=level_dev.id)
            switch2 = Device(name="Switch 2", type="pc", x=2000, y=2000, id_level=level_dev.id)
            session.add(switch1)
            session.add(switch2)
            session.commit()
    # if there are cables with devices id that are < 0 then delete them as they were in a placing state when the game closed
    with Session(engine) as session:
        cables = session.exec(select(Cable)).all()
        for cable in cables:
            if cable.id_device_1 < 0:
                session.delete(cable)
        session.commit()


init()
