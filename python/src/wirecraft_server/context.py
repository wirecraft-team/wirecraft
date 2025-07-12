from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Literal

MISSING: Any = object()


class Context:
    instance: Context | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Context:  # noqa: PYI034
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.debug_options: Sequence[str] = MISSING
        self.bind: str = MISSING
        self.database: str = MISSING
        self.database_type: Literal["sqlite", "postgresql"] = MISSING
        self.reset_database: bool = MISSING

    def set(
        self,
        debug_options: Sequence[str],
        bind: str,
        database: str,
        database_type: Literal["sqlite", "postgresql"],
        reset_database: bool,
    ) -> None:
        self.debug_options = debug_options
        self.bind = bind
        self.database = database
        self.database_type = database_type
        self.reset_database = reset_database


ctx = Context()
