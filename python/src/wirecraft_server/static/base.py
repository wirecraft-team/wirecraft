from __future__ import annotations

from pydantic import BaseModel, Field

from .tests import Test


class Level(BaseModel):
    id: int
    tasks: list[Task]


class Task(BaseModel):
    name: str
    description: str
    completed: bool | None = None
    error_message: str | None = None
    tests: list[Test] = Field(exclude=True)
