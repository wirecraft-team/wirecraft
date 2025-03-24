from __future__ import annotations

from pydantic import BaseModel


class Level(BaseModel):
    id: int
    tasks: list[Task] = []


class Task(BaseModel):
    ref: str
    level_id: int
    name: str
    description: str
    completed: bool = False


task0_1 = Task(ref="task0_1", level_id=0, name="task0_1", description="This is task 0_1")
task0_2 = Task(ref="task0_2", level_id=0, name="task0_2", description="This is task 0_2")

task1_1 = Task(ref="task1_1", level_id=1, name="task1_1", description="This is task 1_1")
task1_2 = Task(ref="task1_2", level_id=1, name="task1_2", description="This is task 1_2")
task1_3 = Task(ref="task1_3", level_id=1, name="task1_3", description="This is task 1_3")


level0 = Level(id=0, tasks=[task0_1, task0_2])
level1 = Level(id=1, tasks=[task1_1, task1_2, task1_3])
level2 = Level(id=2, tasks=[])
