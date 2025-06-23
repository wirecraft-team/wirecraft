from __future__ import annotations

from pydantic import BaseModel


class Level(BaseModel):
    id: int
    tasks: list[Task]


class Task(BaseModel):
    name: str
    description: str
