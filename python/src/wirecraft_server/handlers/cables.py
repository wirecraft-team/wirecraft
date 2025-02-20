from __future__ import annotations

from pydantic import BaseModel

from wirecraft_server.handlers_core import Handler, event


class PingData(BaseModel):
    content: str


class CablesHandler(Handler):
    @event
    async def ping(self, data: PingData):
        print(self)
        print(data)
        print(data.content)
        print("pinged")
