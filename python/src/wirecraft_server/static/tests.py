from collections.abc import Sequence
from ipaddress import IPv4Address

from pydantic import BaseModel

from ..database.models import Device
from ..networking.device import NetworkDevice
from ..networking.requests import send_ping


class TestFailure(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class Test(BaseModel):
    def __call__(
        self,
        devices: Sequence[Device],
        network: dict[int, NetworkDevice],
        map_names: dict[str, int],
    ) -> None:
        raise NotImplementedError


class DevicePresenceTest(Test):
    name: str
    type: str

    def __call__(
        self,
        devices: Sequence[Device],
        network: dict[int, NetworkDevice],
        map_names: dict[str, int],
    ):
        for device in devices:
            if device.name == self.name:
                if device.type == self.type:
                    return
                raise TestFailure(f"Device {self.name} found, but it is of type {device.type}, expected {self.type}.")

        raise TestFailure(f"Device {self.name} of type {self.type} not found in the network.")


class CableConnectionTest(Test):
    source: str
    destination: str

    def __call__(self, devices: Sequence[Device], network: dict[int, NetworkDevice], map_names: dict[str, int]) -> None:
        source_device_id = map_names.get(self.source)
        destination_device_id = map_names.get(self.destination)

        if source_device_id is None:
            raise TestFailure(f"Source device '{self.source}' not found in the network.")
        if destination_device_id is None:
            raise TestFailure(f"Destination device '{self.destination}' not found in the network.")

        source_device = network[source_device_id]
        destination_device = network[destination_device_id]

        if destination_device not in source_device.connected_devices:
            raise TestFailure(f"Device {self.source} is not connected to {self.destination}.")


class PingTest(Test):
    source: str
    destination: IPv4Address

    def __call__(
        self,
        devices: Sequence[Device],
        network: dict[int, NetworkDevice],
        map_names: dict[str, int],
    ):
        source_device_id = map_names.get(self.source)
        if source_device_id is None:
            raise TestFailure(f"Source device '{self.source}' not found in the network.")

        source_device = network[source_device_id]
        response = send_ping(source_device, self.destination)
        if not response:
            raise TestFailure(f"Ping from {self.source} to {self.destination} failed.")
