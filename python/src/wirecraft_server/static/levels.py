from .base import Level, Task

levels = [
    Level(
        id=0,
        tasks=[
            Task(
                name="task0_1",
                description="This is task 0_1",
            ),
            Task(
                name="task0_2",
                description="This is task 0_2",
            ),
        ],
    ),
    Level(
        id=1,
        tasks=[
            Task(
                name="task1_1",
                description="This is task 1_1",
            ),
            Task(
                name="task1_2",
                description="This is task 1_2",
            ),
        ],
    ),
]
