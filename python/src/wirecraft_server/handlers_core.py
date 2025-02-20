# TODO(airopi): add comments & documentation

from __future__ import annotations

import inspect
import typing
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Self

from pydantic import BaseModel

if TYPE_CHECKING:
    from wirecraft_server.server import Server

    type DataEventCallbackT[H: Handler, T: BaseModel] = Callable[[H, T], Any]
    type SimpleEventCallbackT[H: Handler] = Callable[[H], Any]
    type EventCallbackT[H: Handler, T: BaseModel] = DataEventCallbackT[H, T] | SimpleEventCallbackT[H]


class Event[H: Handler, T: BaseModel]:
    def __init__(self, type: str, data_type: type[T] | None, func: EventCallbackT[H, T]):
        self.type = type
        self.data_type = data_type
        self.callback = func
        self.handler: H | None = None

    async def __call__(self, data: str) -> Any:
        if self.handler is None:
            raise ValueError("Event handler not set.")

        if self.data_type is None:
            return await self.callback(self.handler)  # pyright: ignore[reportCallIssue]
        else:
            parsed_data = self.data_type.model_validate(data)  # TODO(airopi): add error handling
            return await self.callback(self.handler, parsed_data)  # pyright: ignore[reportCallIssue]


class HandlerMeta(type):
    __handler_events__: set[Event[Any, Any]]

    def __new__(cls, *args: Any, **kwargs: Any) -> HandlerMeta:
        name, bases, attrs = args
        new_cls = super().__new__(cls, name, bases, attrs, **kwargs)
        new_cls.__handler_events__ = set()
        for base in reversed(new_cls.__mro__):
            for value in base.__dict__.values():
                if isinstance(value, Event):
                    new_cls.__handler_events__.add(value)  # pyright: ignore[reportUnknownArgumentType]
        return new_cls


class Handler(metaclass=HandlerMeta):
    __handler_events__: set[Event[Any, Any]]

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        self = super().__new__(cls)
        self.__handler_events__ = cls.__handler_events__
        for event in self.__handler_events__:
            event.handler = self
        return self

    def __init__(self, server: Server):
        self.server = server


def event[H: Handler, T: BaseModel](f: EventCallbackT[H, T]) -> Event[H, T]:
    annotations = typing.get_type_hints(f)
    signature = inspect.signature(f)
    _, *parameters = signature.parameters
    model = None if not parameters else annotations[parameters[0]]

    return Event(
        f.__name__.upper(),
        model,
        f,
    )
