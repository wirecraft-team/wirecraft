from ipaddress import IPv4Address

from .capabilities import ARPCapability, IPv4Capability, Routing
from .device import NetworkDevice
from .mac_address import MacAddress
from .osi import ARPOpCode, ARPPacket, EthernetFrame, ICMPMessage, ICMPType, IPv4Packet


def send_arp_request(source: NetworkDevice, target_ip: IPv4Address):
    """Send an ARP request to resolve the MAC address of a target IP."""
    source.log(f"Sending ARP request for IP {target_ip}")
    source.log(f"Resolving the route for {target_ip}")
    routing_cap = source.get_capability(Routing)
    if routing_cap is None:
        source.log("No routing capability found, cannot send ARP request")
        raise ValueError("No routing capability found")

    arp_cap = source.get_capability(ARPCapability)
    if arp_cap is None:
        source.log("No ARP capability found, cannot send ARP request")
        raise ValueError("No ARP capability found")

    ipv4_cap = source.get_capability(IPv4Capability)
    if ipv4_cap is None:
        source.log("No IPv4 capability found, cannot send ARP request")
        raise ValueError("No IPv4 capability found")

    route = routing_cap.routing_table.get_route(target_ip)
    if route is None:
        source.log(f"No route found for {target_ip}")
        raise ValueError("No route to destination")

    if route.gateway is not None:
        source.log(f"The route for {target_ip} goes through a gateway, which is not allowed for ARP requests.")
        raise ValueError("ARP requests should be sent to a directly connected device, not through a gateway")

    device = source.connected_devices.inverse.get(route.interface)
    if device is None:
        source.log(f"No device connected on the specified interface {route.interface}")
        return

    source.log(f"Sending ARP request through the interface {route.interface} to {device}")
    request = EthernetFrame(
        destination_mac=MacAddress.broadcast(),
        source_mac=source.mac_address,
        payload=ARPPacket(
            opcode=ARPOpCode.REQUEST,
            sender_mac=source.mac_address,
            sender_ip=ipv4_cap.ip_address,
            target_mac=None,
            target_ip=target_ip,
        ),
    )
    response = device.handle_request(source, request)
    if response and isinstance(response.payload, ARPPacket) and response.payload.opcode is ARPOpCode.REPLY:
        source.log(
            f"Got response from {device}: the MAC address for {response.payload.sender_ip} is {response.payload.sender_mac}"
        )
        arp_cap.arp_table.set(response.payload.sender_ip, response.payload.sender_mac)
    else:
        source.log(f"No response or invalid response received for ARP request for {target_ip}")


def send_ping(source: NetworkDevice, target_ip: IPv4Address):
    source.log(f"Sending ping to {target_ip}")

    routing_cap = source.get_capability(Routing)
    if routing_cap is None:
        source.log("No routing capability found, cannot send ARP request")
        raise ValueError("No routing capability found")

    arp_cap = source.get_capability(ARPCapability)
    if arp_cap is None:
        source.log("No ARP capability found, cannot send ARP request")
        raise ValueError("No ARP capability found")

    ipv4_cap = source.get_capability(IPv4Capability)
    if ipv4_cap is None:
        source.log("No IPv4 capability found, cannot send ARP request")
        raise ValueError("No IPv4 capability found")

    route = routing_cap.resolve_route(target_ip)
    if route is None:
        return False

    if route.gateway is None:
        source.log(f"Using direct connection to {target_ip}")
        target_ip = target_ip
    else:
        source.log(f"Using gateway {route.gateway} for {target_ip}")
        target_ip = route.gateway

    target_mac = arp_cap.resolve_mac(target_ip)
    if target_mac is None:
        return False

    icmp_packet = ICMPMessage(type=ICMPType.ECHO_REQUEST)
    ipv4_packet = IPv4Packet(
        ttl=64,
        source_ip=ipv4_cap.ip_address,
        destination_ip=target_ip,
        payload=icmp_packet,
    )
    ethernet_frame = EthernetFrame(
        destination_mac=target_mac,
        source_mac=source.mac_address,
        payload=ipv4_packet,
    )
    device = source.connected_devices.inverse.get(route.interface)
    if device is None:
        raise ValueError("No device connected on the specified interface")

    source.log(f"Sending ICMP Echo Request through the interface {route.interface}")
    response = device.handle_request(source, ethernet_frame)
    if response is None:
        source.log("No response received")
        return False

    if (
        isinstance(response.payload, IPv4Packet)
        and isinstance(response.payload.payload, ICMPMessage)
        and response.payload.payload.type is ICMPType.ECHO_REPLY
    ):
        source.log(f"Received ICMP Echo Reply from {target_ip}")
        return True
    else:
        source.log(f"Received unexpected response: {response.payload}")
        return False
