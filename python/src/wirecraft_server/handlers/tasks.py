from __future__ import annotations

from collections.abc import Sequence

from pydantic import BaseModel

from ..database.base import Task, list_level
from ..handlers_core import Handler, event


class GetLevelTasksData(BaseModel):
    """
    Payload for the get_level_tasks event.
    """

    level_id: int


class TasksHandler(Handler):
    @event
    async def get_level_tasks(self, data: GetLevelTasksData) -> Sequence[Task]:
        level = list_level[data.level_id]
        return level.tasks
