from scapy.all import ARP, Ether, srp
from typing import List, Dict
import ipaddress

def get_devices_on_network(network: str) -> List[Dict[str, str]]:
    """
    Scans the local network for devices using ARP.

    Args:
    - network (str): The network range to scan, e.g., "192.168.1.1/24".

    Returns:
    - List[Dict[str, str]]: A list of devices found, each with 'ip' and 'mac' addresses.
    """
    devices = []
    # IP Network to CIDR conversion for Scapy compatibility
    try:
        ip_net = ipaddress.ip_network(network, strict=False)
    except ValueError as e:
        print(f"Invalid network address: {e}")
        return devices

    # Create ARP request packet
    arp_req = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=str(ip_net))
    # Send the packet and receive responses
    ans, _ = srp(arp_req, timeout=2, verbose=False)

    for sent, received in ans:
        devices.append({"ip": received.psrc, "mac": received.hwsrc})

    return devices

# Example usage
network_range = "192.168.1.0/24"  # Adjust to your network range
devices = get_devices_on_network(network_range)
for device in devices:
    print(f"IP: {device['ip']}, MAC: {device['mac']}")
