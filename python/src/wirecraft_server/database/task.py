from .models import Level, Task

level0 = Level(completed=False)
level1 = Level(completed=False)
level2 = Level(completed=False)

task1_l0 = Task(id_level=level0.id, name="T1 l0", description="Task1 level0")
task2_l0 = Task(id_level=level0.id, name="T2 l0", description="Task2 level0")
task3_l0 = Task(id_level=level0.id, name="T3 l0", description="Task3 level0")

task1_l1 = Task(id_level=level1.id, name="T1 l1", description="Task1 level1")
task2_l1 = Task(id_level=level1.id, name="T2 l1", description="Task2 level1")
task3_l1 = Task(id_level=level1.id, name="T3 l1", description="Task3 level1")
