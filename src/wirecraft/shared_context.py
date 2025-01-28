from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wirecraft.server.server import Server

server_var: ContextVar[Server] = ContextVar("server")
