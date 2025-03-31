from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class Port(BaseModel):
    type: Literal["RJ45", "SFP"]  # type of the port (RJ45, SFP, ...)
    speed: int  # speed of the port (MB/s)
    PoE: bool  # does the port have PoE capabilities?


class Switch(BaseModel):
    PoE: bool  # does the switch have PoE support?
    capacity: int  # switching capacity in Mbps


class Router(BaseModel):
    firewall: bool  # does the router have a firewall?
    capacity: int  # routing capacity in Mbps


class Host(BaseModel):
    ram: int  # in GB
    cpu: int  # in "score points"
    storage: int  # in GB


class Device(BaseModel):
    features: list[Host | Switch | Router]  # list of features of the device
    name: str  # name of the device
    ports: list[Port]  # list of ports
    price: int  # price of the device


class Service(BaseModel):
    type: str  # type of service (website, mail server, ...)
    name: str  # name of the service
    state: bool  # state of the service (running or not)


class Cable(BaseModel):
    type: str  # type of the cable (RJ45, SFP, ...)
    speed: int  # speed of the cable (MB/s)


class Level(BaseModel):
    id: int


class Task(BaseModel):
    ref: str
    level_id: int  # Foreign key to Level.id
    name: str
    description: str


first_pc = Device(
    features=[Host(ram=4, cpu=10, storage=256)],
    name="pc1",
    ports=[
        Port(type="RJ45", speed=250, PoE=False),
    ],
    price=1000,
)
first_switch = Device(
    features=[Switch(PoE=False, capacity=1000)],
    name="sw1",
    # 8 RJ45 ports
    ports=[Port(type="RJ45", speed=1000, PoE=False) for _ in range(8)],
    price=500,
)

device_list = [first_pc, first_switch]
device_dict = {d.name: d for d in device_list}

# Task declaration
task0_1 = Task(
    ref="task0_1",
    level_id=0,
    name="task0_1",
    description="This is task 0_1",
)
task0_2 = Task(
    ref="task0_2",
    level_id=0,
    name="task0_2",
    description="This is task 0_2",
)

task1_1 = Task(
    ref="task1_1",
    level_id=1,
    name="task1_1",
    description="This is task 1_1",
)
task1_2 = Task(
    ref="task1_2",
    level_id=1,
    name="task1_2",
    description="This is task 1_2",
)
task1_3 = Task(
    ref="task1_3",
    level_id=1,
    name="task1_3",
    description="This is task 1_3",
)


level0 = Level(id=0)
level1 = Level(id=1)
level2 = Level(id=2)
