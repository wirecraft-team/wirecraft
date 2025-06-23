from ipaddress import IPv4Network

from networking import IPv4Address, MacAddress
from networking.capabilities import (
    ARPCapability,
    BasicEthernetFrameCapability,
    ICMPCapability,
    IPv4Capability,
    Layer2Switching,
    Routing,
)
from networking.device import (
    IPNetworkDevice,
    NetworkDevice,
)
from networking.requests import send_ping

computer_a = IPNetworkDevice(
    ip_address=IPv4Address("192.168.0.2"),
    mac_address=MacAddress("00:11:22:33:44:55"),
)
routing_a = Routing()
routing_a.routing_table.add_route(IPv4Network("192.168.0.0/24"))
computer_a.add_capability(
    BasicEthernetFrameCapability(), routing_a, ARPCapability(), IPv4Capability(), ICMPCapability()
)

routing_b = Routing()
routing_b.routing_table.add_route(IPv4Network("192.168.0.0/24"))
computer_b = IPNetworkDevice(
    mac_address=MacAddress("66:77:88:99:AA:BB"),
    ip_address=IPv4Address("192.168.0.3"),
)
computer_b.add_capability(
    BasicEthernetFrameCapability(), routing_b, ARPCapability(), IPv4Capability(), ICMPCapability()
)


layer_2_switch = NetworkDevice(mac_address=MacAddress("CC:DD:EE:FF:00:11"))
layer_2_switch.add_capability(Layer2Switching())

computer_a.add_connection(0, layer_2_switch, 1)
computer_b.add_connection(0, layer_2_switch, 2)


if send_ping(computer_a, IPv4Address("192.168.0.3")):
    print("Ping successful!")
else:
    print("Ping failed!")
