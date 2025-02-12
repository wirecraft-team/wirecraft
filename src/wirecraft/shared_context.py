from __future__ import annotations

from collections.abc import Sequence
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from wirecraft.server.server import Server

server_var: ContextVar[Server] = ContextVar("server")


class Context:
    instance: Context | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Context:  # noqa: PYI034
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.debug_options: Sequence[str] = []

    def set(self, debug_options: Sequence[str] | None = None) -> None:
        if debug_options is not None:
            self.debug_options = debug_options


ctx = Context()
