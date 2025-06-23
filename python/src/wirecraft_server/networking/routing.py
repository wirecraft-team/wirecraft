from __future__ import annotations

from ipaddress import IPv4Address, IPv4Network

from pydantic import BaseModel, Field


class Route(BaseModel):
    destination: IPv4Network
    gateway: IPv4Address | None = None
    interface: int  # Interfaces are ports number in our simplified model


# @dataclass(kw_only=True, eq=False, repr=False)
class RoutingTable(BaseModel):
    table: list[Route] = Field(default_factory=list[Route])

    def add_route(self, destination: IPv4Network, gateway: IPv4Address | None = None, interface: int = 0):
        """
        Add a route to the routing table.
        """
        self.table.append(Route(destination=destination, gateway=gateway, interface=interface))

    def get_route(self, target: IPv4Address) -> Route | None:
        """
        Find a route for a given destination IP address.
        """
        for route in self.table:
            if target in route.destination:
                return route
        return None
