import ipaddress
import os
import platform
import re
import subprocess
import psutil
import requests
import ctypes
from typing import Any, Callable, Dict, List, Optional
from xml.dom import ValidationErr
from ..commands import Command, CommandArgs, ICommandModule, CommandResult
from pydantic import Field
from scapy.all import ARP, Ether, srp


class NetworkScanArgs(CommandArgs):
    network: str = Field("192.168.1.0/24", json_schema_extra={"description" : "Network range to scan"})

command_arg_map = {
    Command.GET_DEVICES_ON_NETWORK : NetworkScanArgs,
    Command.GET_ADAPTER_STATS: None,
    Command.GET_ADAPTERS: None,
    Command.GET_WIFI_NETWORKS: None,
    Command.GET_WIFI_PASSWORDS: None,
    Command.GET_IP_INFO: None,
    Command.GET_COUNTRY: None,
    Command.GET_PUBLIC_IP: None,
}

class NetworkInfo(ICommandModule):
    def __init__(self) -> None:
        self.ip = self._get_public_ip()
        
    def _get_public_ip(self, provider: str = "https://api.ipify.org") -> str:
        try:
            response = requests.get(provider)
            response.raise_for_status()  # This will raise an exception for HTTP errors
            return response.text
        except Exception as e:
            return None
        
    def get_ip(self) -> CommandResult:
        if self.ip:
            return CommandResult(result=self.ip, success=True)
        else:
            return CommandResult(result="No IP Found", success=False)

    def get_country(self) -> CommandResult:
        if not self.ip:
            return CommandResult(result="IP Address not available", success=False)
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}?fields=country")
            response.raise_for_status()
            data = response.json()
            country = data.get("country")
            if country:
                return CommandResult(result=data["country"], success=True)
            else:
                return CommandResult(result="Failed to retrieve country", success=False)
        except Exception as e:
            return CommandResult(result=str(e), success=False)

    def get_ip_info(self) -> CommandResult:
        if not self.ip:
            return CommandResult(result="IP Address not available", success=False)
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query")
            response.raise_for_status()
            data = response.json()
            if data.get("status") == "success":
                return CommandResult(result=data, success=True)
            else:
                return CommandResult(result=data.get("message", "Failed to retrieve IP information"), success=False)
        except Exception as e:
            return CommandResult(result=str(e), success=False)

    def is_admin(self):
        if platform.system() == "Windows":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
        else:
            return os.geteuid() == 0
        
    def get_wifi_passwords(self) -> CommandResult:
        os_type = platform.system()
        passwords = {}

        if os_type == "Windows":
            data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], encoding='utf-8', errors='ignore').split('\n')
            profiles = [i.split(":")[1].strip() for i in data if "All User Profile" in i]
            for profile in profiles:
                try:
                    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], encoding='utf-8', errors='ignore').split('\n')
                    password_lines = [b.split(":")[1].strip() for b in results if "Key Content" in b]
                    if password_lines:
                        passwords[profile] = password_lines[0]
                except subprocess.CalledProcessError:
                    pass
        else:
            return CommandResult(success=False, result=f"Retrieving WiFi passwords is not supported on {os_type} through this method.")


        return passwords
    
    def parse_linux_wifi_networks(self, output: str) -> List[Dict[str, str]]:
        networks: List[Dict[str, str]] = []
        lines = output.strip().split('\n')[1:]  # Skip the header line with [1:]
        for line in lines:
            # Skip lines that are separators or don't contain useful data
            if '--' in line:
                continue
            # Use the adjusted regex to capture SSID and SECURITY, excluding lines with insufficient spacing
            match = re.match(r"([^\s].*?)\s{2,}(\S.*)", line.strip())
            if match:
                ssid, security = match.groups()
                # Trim extra spaces from security for cleaner output
                networks.append({'SSID': ssid, 'Security': security.strip()})
        return networks

    def get_wifi_networks(self) -> CommandResult:
        os_type = platform.system()
        networks: List[Dict[str, Any]] = []

        if os_type == "Windows":
            try:
                data: str = subprocess.check_output(['netsh', 'wlan', 'show', 'network', 'mode=bssid'], encoding='utf-8').split('\nSSID')
                for ssid in data[1:]:
                    ssid_info = {'SSID': None, 'Security': None}
                    for line in ssid.split('\n'):
                        if "SSID name" in line:
                            ssid_info['SSID'] = line.split(":")[1].strip()
                        if "Authentication" in line:
                            ssid_info['Security'] = line.split(":")[1].strip()
                    networks.append(ssid_info)
            except subprocess.CalledProcessError as e:
                return CommandResult(success=False, result=f"Error: {e}")

        elif os_type == "Linux":
            if not self.is_admin():
                return CommandResult(success=False, result=f"Error: Admin previliges needed")
            try:
                output: str = subprocess.check_output("nmcli -f SSID,SECURITY dev wifi", shell=True, encoding='utf-8')
                networks = self.parse_linux_wifi_networks(output)
            except subprocess.CalledProcessError as e:
                return CommandResult(success=False, result=f"Error :{e}")

        return CommandResult(success=True, result=networks)

    def get_devices_on_network(self, args: NetworkScanArgs) -> CommandResult:
        """
        Scans the local network for devices using ARP.

        :param network: The network range to scan, e.g., "192.168.1.1/24".
        :return: CommandResult object with success status and list of devices or error message.
        """
        try:
            ip_net = ipaddress.ip_network(args.network, strict=False)
        except ValueError as e:
            return CommandResult(success=False, result=f"Invalid network address: {e}")
        
        os_type = platform.system()
        if os_type == "Linux":
            if not self.is_admin():
                return CommandResult(success=False, result=f"Admin previlages needed")

        try:
            arp_req = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(ip_net))
            ans, _ = srp(arp_req, timeout=2, verbose=False, iface_hint=str(ip_net.network_address))

            devices: List[Dict[str, str]] = []
            for sent, received in ans:
                devices.append({"ip": received.psrc, "mac": received.hwsrc})

            if devices:
                return CommandResult(success=True, result=devices)
            else:
                return CommandResult(success=False, result="No devices found on the network.")
        except Exception as e:
            return CommandResult(success=False, result=f"Error: {e}")

    @staticmethod
    def get_adapters() -> CommandResult:
        try:
            addresses = psutil.net_if_addrs()
            adapters = {intface: addrs for intface, addrs in addresses.items()}
            return CommandResult(success=True, result=adapters)
        except Exception as e:
            return CommandResult(success=False, result=f"Failed to get adapters: {str(e)}")

    @staticmethod
    def get_adapter_stats() -> CommandResult:
        try:
            stats = psutil.net_if_stats()
            adapter_stats = {intface: {"isup": stat.isup, "duplex": stat.duplex, "speed": stat.speed, "mtu": stat.mtu} for intface, stat in stats.items()}
            return CommandResult(success=True, result=adapter_stats)
        except Exception as e:
            return CommandResult(success=False, result=f"Failed to get adapter stats: {str(e)}")

    def run(self, command: Command, args: Optional[CommandArgs] = None) -> CommandResult:
        command_func_map: Dict[Command, Callable[[], CommandResult]] = {
            Command.GET_ADAPTER_STATS: self.get_adapter_stats,
            Command.GET_ADAPTERS: self.get_adapters,
            Command.GET_WIFI_NETWORKS: self.get_wifi_networks,
            Command.GET_WIFI_PASSWORDS: self.get_wifi_passwords,
            Command.GET_IP_INFO: self.get_ip_info,
            Command.GET_COUNTRY: self.get_country,
            Command.GET_PUBLIC_IP: self.get_ip,
        }
        command_func_map_with_args = {
            Command.GET_DEVICES_ON_NETWORK : self.get_devices_on_network
        }

        # Handle commands that require arguments separately
        if command in command_func_map_with_args:
            if args is None:
                return CommandResult(success=False, result="No Args passed")
            try:
                validated_args = command_arg_map[command](**args.model_dump())
                return command_func_map_with_args[command](validated_args)
            except ValidationErr as e:
                return CommandResult(success=False, result=f"Validation error: {e}")

        # Handle no-arg commands
        if command in command_func_map:
            try:
                return command_func_map[command]()
            except Exception as e:
                return CommandResult(success=False, result=f"Error executing command: {e}")

        return CommandResult(success=False, result="Command not found in module or invalid arguments provided.")


