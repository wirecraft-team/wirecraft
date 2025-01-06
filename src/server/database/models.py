from typing import Optional

from sqlmodel import Field, SQLModel




class Cable(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    id_device_A : int = Field(default=None, foreign_key="Device.id")
    port_A : int
    id_device_B: int = Field(default=None, foreign_key="Device.id")
    port_B : int

class Device(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    type: str
    x: int
    y: int


