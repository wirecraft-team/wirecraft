from __future__ import annotations

from ipaddress import IPv4Address

from pydantic import Field

from ..routing import Route, RoutingTable
from .base import Capability


class Routing(Capability):
    routing_table: RoutingTable = Field(init=False, default_factory=RoutingTable)

    def resolve_route(self, target_ip: IPv4Address) -> Route | None:
        self._device.log(f"Resolving the route for {target_ip}")
        route = self.routing_table.get_route(target_ip)
        if route is None:
            self._device.log(f"No route found for {target_ip}")
        self._device.log(f"Route found: {route}")
        return route
