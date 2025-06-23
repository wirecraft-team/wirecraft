from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import PrivateAttr

from ..device import IPNetworkDevice, NetworkDevice
from ..osi import ICMPMessage, ICMPType
from .base import Capability


class ICMPCapability(Capability):
    handle = ICMPMessage
    device_type = IPNetworkDevice
    if TYPE_CHECKING:
        _device: IPNetworkDevice = PrivateAttr()  # type: ignore

    def __call__(self, source: NetworkDevice, message: ICMPMessage) -> ICMPMessage | None:
        self._device.log(f"Handling ICMP message from {source.mac_address}")

        if message.type is ICMPType.ECHO_REQUEST:
            self._device.log("Received ICMP Echo Request, sending Echo Reply")
            return ICMPMessage(type=ICMPType.ECHO_REPLY)
        elif message.type == ICMPType.ECHO_REPLY:
            # In our model, we should never receive an Echo reply through the handle_request method
            self._device.log("Received ICMP Echo Reply")
            return None
