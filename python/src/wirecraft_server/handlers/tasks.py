from __future__ import annotations

from collections.abc import Sequence

from pydantic import BaseModel
from uv import TYPE_CHECKING

from ..handlers_core import Handler, event
from ..static import levels

if TYPE_CHECKING:
    from ..static.base import Task


class GetLevelTasksData(BaseModel):
    """
    Payload for the get_level_tasks event.
    """

    level_id: int


class TasksHandler(Handler):
    @event
    async def get_level_tasks(self, data: GetLevelTasksData) -> Sequence[Task]:
        level = levels[data.level_id]
        return level.tasks
