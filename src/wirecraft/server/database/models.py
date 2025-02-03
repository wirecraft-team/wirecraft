from sqlmodel import (
    Field,  # type: ignore
    Session,
    SQLModel,
    create_engine,
)

engine = create_engine("sqlite:///database.db", echo=True)


class Cable(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    id_device_1: int = Field(default=None, foreign_key="device.id")  # Lowercase
    port_1: int
    id_device_2: int = Field(default=None, foreign_key="device.id")  # Lowercase
    port_2: int


class Device(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    type: str
    x: int
    y: int
    id_level: int | None = Field(default=None, foreign_key="level.id")  # Lowercase


class Level(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    completed: bool = False


class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    id_level: int | None = Field(default=None, foreign_key="level.id")  # Lowercase
    name: str
    completed: bool = False


def init():
    SQLModel.metadata.create_all(engine)
    level_dev = Level(completed=False)
    # Add level first to get an ID before assigning it to devices
    with Session(engine) as session:
        session.add(level_dev)
        session.commit()
        session.refresh(level_dev)

        switch1 = Device(name="Switch 1", type="switch", x=0, y=0, id_level=level_dev.id)
        switch2 = Device(name="Switch 2", type="switch", x=200, y=200, id_level=level_dev.id)
        session.add(switch1)
        session.add(switch2)
        session.commit()
