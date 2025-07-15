from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import time
import urllib.parse
from pathlib import Path
from typing import Any, Self

from aiohttp import WSMessage, WSMsgType, web
from pydantic_core import from_json, to_json
from sqlalchemy.ext.asyncio import create_async_engine

from .context import ctx
from .database import init_db
from .database.session import async_session
from .handlers import CablesHandler, DevicesHandler, LaunchHandler, TasksHandler
from .handlers_core import Handler

TICK_RATE = 20

logger = logging.getLogger(__name__)


class Server:
    """
    This is the core of the server, maintaining the state (current connections, database instance, background tasks...)
    """

    def __init__(self) -> None:
        self._current_tick = 0
        self.client_connexions: set[web.WebSocketResponse] = set()
        self._last_refresh: float = time.perf_counter()

        # nb: if this event is set, the server will stop
        # This is used if we *need* to stop the server in any other way than CTRL+C
        # Or if we have tasks that need to finish properly before stopping, so they know they should stop without having
        # to cancel them.
        self._stop = asyncio.Event()

        self.handlers: list[Handler] = [
            CablesHandler(self),
            DevicesHandler(self),
            TasksHandler(self),
            LaunchHandler(self),
        ]

    def start(self):
        logger.info("Server started!")
        try:
            asyncio.run(self._run())
        except KeyboardInterrupt:
            logger.info("Server stopped!")
            self._stop.set()  # if some tasks depends on this event
        except Exception:
            logger.exception("Server crashed!")
            raise SystemExit(1)

    async def _wait_next_refresh(self):
        """This method allow the server to do background tasks at a fixed rate."""
        delay = 1 / TICK_RATE
        _next = self._last_refresh + delay
        _now = time.perf_counter()
        _wait = _next - _now
        if _wait < 0:
            # TODO(airopi): implement server slow down (increase delay in case of poor performances)
            # logger.warning("Can't keep up ! %ss behind the normal refresh", -round(_wait, 3))
            self._last_refresh = _now
            return self._stop.is_set()

        self._last_refresh = _next
        with contextlib.suppress(asyncio.TimeoutError):
            await asyncio.wait_for(self._stop.wait(), _wait)
        return self._stop.is_set()

    def _connect(self, ws: web.WebSocketResponse) -> Self:
        """Handle a new client connection."""
        self.client_connexions.add(ws)
        logger.debug("New client connected")
        return self

    def _disconnect(self, ws: web.WebSocketResponse):
        """Handle a client disconnection."""
        self.client_connexions.remove(ws)
        logger.debug("Client disconnected")

    async def _websocket_handler(self, request: web.Request):
        """
        There is an "websocket_handler" running per client.
        This task maintain the connection and receive the messages from the client.
        """
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        self._connect(ws)
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    logger.debug("Received: %s", data)
                    await self._handle_message(msg)
        except Exception:
            logger.exception("Client error")
        finally:
            self._disconnect(ws)
        return ws

    async def _handle_message(self, msg: WSMessage):
        """
        Handle the messages received from the client.
        It will search for an handler for the event type and call it.
        """
        data = from_json(msg.data)
        logger.debug("Received: %s", data)
        handled: bool = False
        # Loop is used so multiple handler could handle the same event.
        # This is useful for example if we want to log the event and then handle it.
        for handler in self.handlers:
            # t for type and d for data
            # inspired by https://discord.com/developers/docs/events/gateway-events#payload-structure
            try:
                if event := handler.__handler_events__.get(data["t"]):
                    handled = True
                    await event(data["d"])
            except Exception:
                logger.exception("Error while handling event %s:", data["t"])
                continue

        if not handled:
            logger.warning("Unhandled event: %s", data)

    async def _websocket_helthcheck(self, request: web.Request):
        """
        This is a simple healthcheck endpoint that returns a 200 OK response.
        It can be used to check if the server is running.
        """
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.send_str("OK")
        await ws.close()
        return ws

    async def _run(self):
        if ctx.database_type == "sqlite":
            path = Path(ctx.database)
            resolved = path.resolve()
            encoded_path = urllib.parse.quote(str(resolved))
            db = f"sqlite+aiosqlite:///{encoded_path}"
        elif ctx.database_type == "postgresql":
            db = f"postgresql+asyncpg://{ctx.database}"
        else:
            raise ValueError(f"Unsupported database type: {ctx.database_type}")

        engine = create_async_engine(db)
        async_session.configure(bind=engine)
        await init_db(engine)

        self.app = web.Application()
        self.app.router.add_get("/", self._websocket_handler)
        self.app.router.add_get("/health", self._websocket_helthcheck)
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, ctx.bind, 8765)
        await self.site.start()

        logger.info("WebSocket server started on ws://%s0:8765", ctx.bind)

        while True:
            stopped = await self._wait_next_refresh()
            if stopped:
                logger.info("Server stopped!")
                break
            # await update_devices()
            # await update_routing_tables()
            # print(global_device_list[1].ping("192.168.1.3"))
            await self._tick()

    async def broadcast_json(self, data: Any):
        await self.broadcast(to_json(data))

    async def broadcast(self, message: bytes):
        """
        Send message to all connected clients.
        """
        if self.client_connexions:
            await asyncio.gather(*[ws.send_bytes(message) for ws in self.client_connexions])

    async def _tick(self):
        """
        This can be activated to tell the client what is the current tick.
        """
        self._current_tick += 1
        if self._current_tick % 60 == 0:
            # await self.broadcast_json({"t": "TICK_EVENT", "d": self._current_tick})
            pass
