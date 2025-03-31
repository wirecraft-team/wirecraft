from __future__ import annotations

from collections.abc import Sequence

from pydantic import BaseModel
from sqlmodel import select

from ..database.base import Task
from ..database.models import async_session
from ..handlers_core import Handler, event


class GetLevelTasksData(BaseModel):
    """
    Payload for the get_level_tasks event.
    """

    level_id: int


class TasksHandler(Handler):
    @event
    async def get_level_tasks(self, data: GetLevelTasksData) -> Sequence[Task]:
        task_list = select(Task).where(Task.level_id == data.level_id)
        async with async_session() as session:
            result = await session.exec(task_list)
            tasks = result.all()
        return tasks
