from wirecraft_server.networking import IPv4Address, IPv4Network, MacAddress, NetworkDevice
from wirecraft_server.networking.capabilities import (
    ARPCapability,
    BasicEthernetFrameCapability,
    ICMPCapability,
    IPv4Capability,
    Layer2Switching,
    Routing,
)
from wirecraft_server.networking.requests import send_ping


def test_direct_ping():
    computer_a = NetworkDevice(
        mac_address=MacAddress("AA:AA:AA:AA:AA:AA"),
    )
    routing_a = Routing()
    routing_a.routing_table.add_route(IPv4Network("192.168.0.0/24"))
    computer_a.add_capability(
        BasicEthernetFrameCapability(),
        routing_a,
        ARPCapability(),
        IPv4Capability(ip_address=IPv4Address("192.168.0.2")),
        ICMPCapability(),
    )

    computer_b = NetworkDevice(
        mac_address=MacAddress("BB:BB:BB:BB:BB:BB"),
    )
    routing_b = Routing()
    routing_b.routing_table.add_route(IPv4Network("192.168.0.0/24"))
    computer_b.add_capability(
        BasicEthernetFrameCapability(),
        routing_b,
        ARPCapability(),
        IPv4Capability(ip_address=IPv4Address("192.168.0.3")),
        ICMPCapability(),
    )

    arp_cap_a = computer_a.get_capability(ARPCapability)
    assert arp_cap_a is not None, "ARP table should be available on computer A"

    arp_cap_b = computer_b.get_capability(ARPCapability)
    assert arp_cap_b is not None, "ARP table should be available on computer B"

    assert send_ping(computer_a, IPv4Address("192.168.0.3")) is False, "Ping should fail before connection!"

    assert arp_cap_a.arp_table.root == {}, "ARP table of A should still be empty"

    computer_a.add_connection(0, computer_b, 0)

    assert send_ping(computer_a, IPv4Address("192.168.0.3")) is True, "Ping should be successful!"

    assert arp_cap_a.arp_table[IPv4Address("192.168.0.3")] == MacAddress("BB:BB:BB:BB:BB:BB"), (
        "ARP table of A should contain the MAC address of computer B"
    )
    assert arp_cap_b.arp_table[IPv4Address("192.168.0.2")] == MacAddress("AA:AA:AA:AA:AA:AA"), (
        "ARP table of B should contain the MAC address of computer A"
    )

    assert send_ping(computer_b, IPv4Address("192.168.0.2")) is True, "Ping should be successful!"
    assert send_ping(computer_a, IPv4Address("192.168.0.4")) is False, "Ping should fail!"


def test_ping_through_switches():
    computer_a = NetworkDevice(
        mac_address=MacAddress("AA:AA:AA:AA:AA:AA"),
    )
    routing_a = Routing()
    routing_a.routing_table.add_route(IPv4Network("192.168.0.0/24"))
    computer_a.add_capability(
        BasicEthernetFrameCapability(),
        routing_a,
        ARPCapability(),
        IPv4Capability(ip_address=IPv4Address("192.168.0.2")),
        ICMPCapability(),
    )

    computer_b = NetworkDevice(
        mac_address=MacAddress("BB:BB:BB:BB:BB:BB"),
    )
    routing_b = Routing()
    routing_b.routing_table.add_route(IPv4Network("192.168.0.0/24"))
    computer_b.add_capability(
        BasicEthernetFrameCapability(),
        routing_b,
        ARPCapability(),
        IPv4Capability(ip_address=IPv4Address("192.168.0.3")),
        ICMPCapability(),
    )

    layer_2_switch_a = NetworkDevice(mac_address=MacAddress("11:11:EE:FF:00:11"))
    layer_2_switch_a.add_capability(Layer2Switching())
    layer_2_switch_b = NetworkDevice(mac_address=MacAddress("22:DD:EE:FF:00:11"))
    layer_2_switch_b.add_capability(Layer2Switching())

    computer_a.add_connection(0, layer_2_switch_a, 0)
    layer_2_switch_a.add_connection(1, layer_2_switch_b, 0)
    layer_2_switch_b.add_connection(1, computer_b, 0)

    assert send_ping(computer_a, IPv4Address("192.168.0.3")) is True, "Ping should be successful!"

    switching_cap = layer_2_switch_a.get_capability(Layer2Switching)
    assert switching_cap is not None, "Layer 2 switching capability should be available on switch A"
    assert switching_cap._mac_address_table[MacAddress("BB:BB:BB:BB:BB:BB")] == 1, (
        "Switch A should have learned the MAC address of computer B on interface 1"
    )
    assert switching_cap._mac_address_table[MacAddress("AA:AA:AA:AA:AA:AA")] == 0, (
        "Switch A should have learned the MAC address of computer A on interface 0"
    )

    arp_cap_a = computer_a.get_capability(ARPCapability)
    assert arp_cap_a is not None, "ARP table should be available on computer A"
    assert arp_cap_a.arp_table[IPv4Address("192.168.0.3")] == MacAddress("BB:BB:BB:BB:BB:BB"), (
        "ARP table of A should contain the MAC address of computer B"
    )

    arp_cap_b = computer_b.get_capability(ARPCapability)
    assert arp_cap_b is not None, "ARP table should be available on computer B"
    assert arp_cap_b.arp_table[IPv4Address("192.168.0.2")] == MacAddress("AA:AA:AA:AA:AA:AA"), (
        "ARP table of B should contain the MAC address of computer A"
    )

    assert send_ping(computer_b, IPv4Address("192.168.0.2")) is True, "Ping should be successful!"
    assert send_ping(computer_a, IPv4Address("192.168.0.4")) is False, "Ping should fail!"
