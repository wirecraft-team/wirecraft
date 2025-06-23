from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

MISSING: Any = object()


class Context:
    instance: Context | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Context:  # noqa: PYI034
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.debug_options: Sequence[str] = MISSING
        self.bind = MISSING
        self.database = MISSING

    def set(self, debug_options: Sequence[str], bind: str, database: Path) -> None:
        self.debug_options = debug_options
        self.bind = bind
        self.database = database


ctx = Context()
