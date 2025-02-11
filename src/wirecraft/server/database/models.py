from sqlmodel import (
    Field,  # type: ignore
    SQLModel,
)


class Cable(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    id_device_1: int = Field(default=None, foreign_key="Device.id")
    port_1: int
    id_device_2: int = Field(default=None, foreign_key="Device.id")
    port_2: int


class Device(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    type: str
    x: int
    y: int


class Level(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    completed: bool = False


class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    id_level: int = Field(default=None, foreign_key="Level.id")
    name: str
    completed: bool = False
