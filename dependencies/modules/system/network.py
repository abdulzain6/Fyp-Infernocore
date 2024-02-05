import psutil
from ..surveillance import *
from requests import get, post
import subprocess
from ..scripting_interface import execute_batch_script
from ...scripts.batch_scripts.system import ping_scan

class NetworkInfo:

    @staticmethod
    def get_public_ip(provider = "https://api.ipify.org"):
        try:
            return get(provider).text
        except:
            return "0.0.0.0"

    @staticmethod
    def get_country(ip):
        try:
            response = post(f"http://ip-api.com/json/{ip}?fields = status, message, country").json()
            return response["country"]
        except:
            return "USA"

    @staticmethod
    def get_ip_info(ip):
        try:
            return post(
                f"http://ip-api.com/json/{ip}?fields = status, message, continent, continentCode, country, countryCode, region, regionName, city, district, zip, lat, lon, timezone, offset, currency, isp, org, as, asname, reverse, mobile, proxy, hosting, query"
            ).json()

        except:
            return {}

    @staticmethod
    def get_wifi_passwords_windows():
        """Gets wifi passwords saved on the computer.

        Returns:
            dict: Contains plaintext passwords saved on the PC.
        """
        passwords = {}
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors = 'ignore').split('\n')
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        for i in profiles:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key = clear']).decode('utf-8', errors = 'ignore').split('\n')
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            passwords[i] = results[0]
        return passwords


    @staticmethod
    def get_wifi_networks_windows():
        """Gets information about all wifi networks in the area
        Returns:
            list: Contains information about ssids, types, auth, encryption and bssids
        """
        ssids = []
        types = []
        auth = []
        encryption = []
        bssids = []
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'network', 'mode = bssid']).decode(errors = "ignore").split('\nSSID')
        for ssid in data[1:]:

            # Seperating basic information
            bigSplit = f"SSID{ssid}".split("BSSID")
            basicInfo = bigSplit[0].split("\n")
            for i in basicInfo:
                if "SSID" in i and "BSSID" not in i:
                    ssids.append(i.split(":")[1][1:].strip())
                elif "Network type" in i:
                    types.append(i.split(":")[1][1:].strip())
                elif "Authentication" in i:
                    auth.append(i.split(":")[1][1:].strip())
                elif "Encryption" in i:
                    encryption.append(i.split(":")[1][1:].strip())

            #Getting BSSID information
            bssidInfoList = []
            for smallSplit in bigSplit[1:]:
                lines = f"BSSID{smallSplit}".split("\n")
                for i in lines:
                    if "BSSID" in i:
                        bssid = i.split(": ")[1].strip()
                    elif "Signal" in i:
                        signals = i.split(":")[1][1:].strip()
                    elif "Radio type" in i:
                        radioTypes = i.split(":")[1][1:].strip()
                    elif "Channel" in i:
                        channels = i.split(":")[1][1:].strip()
                    elif "Basic rates" in i:
                        basicRates = i.split(":")[1][1:].strip()
                    elif "Other rates" in i:
                        otherRates = i.split(":")[1][1:].strip()
                bssidInfoList.append((bssid, signals, radioTypes, channels, basicRates, otherRates))
            bssids.append(bssidInfoList)
        return list(zip(ssids, types, auth, encryption, bssids))
            

    @staticmethod
    def get_devices_on_network(starting_net_id:int, ending_net_id:int, start_host_id:int, end_host_id:int):
        """Used to get the devices on the local network.

        Args:
            starting_net_id (int): Starting value for 192.168.this.1 part
            ending_net_id (int): Ending value for 192.168.this.1 part
            start_host_id (int): Starting value for 192.168.1.this part
            end_host_id (int): Ending value for 192.168.1.this part
        """
        devices = []
        data = execute_batch_script(ping_scan.format(starting_net_id, ending_net_id, start_host_id, end_host_id), True)
        data = data.split("\n")
        for line in data:
            if "Reply from" in line:
                line = line.split("bytes")[0].replace("Reply from ", "")[:-2]
                devices.append(line)
        return devices
        

    @staticmethod
    def get_adapters():
        addresses = psutil.net_if_addrs()
        return [intface for intface, _ in addresses.items()]
    
    @staticmethod
    def get_adapter_stats():
        return psutil.net_if_stats()




