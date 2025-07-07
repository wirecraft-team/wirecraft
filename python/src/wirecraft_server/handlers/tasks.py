from __future__ import annotations

from collections.abc import Sequence

from pydantic import BaseModel

from ..handlers_core import Handler, event
from ..static import levels
from ..static.base import Task


class GetLevelIdData(BaseModel):
    """
    Payload for the get_level_tasks event.
    """

    level_id: int


class TasksHandler(Handler):
    @event
    async def get_level_tasks(self, data: GetLevelIdData) -> Sequence[Task]:
        level = levels[data.level_id]
        return level.tasks


class LevelIdHandler(Handler):
    @event
    async def update_level_id(self, data: GetLevelIdData) -> int:
        """
        Update the current level ID.
        """
        return data.level_id
