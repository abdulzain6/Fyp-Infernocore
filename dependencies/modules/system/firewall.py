import subprocess
import processManagement

class Firewall:
    @staticmethod
    def firewall_on():
        if processManagement.isElevated() != 1:
            return 0
        subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state" , "on"])
        return 1
        
    @staticmethod
    def firewall_off():
        if processManagement.isElevated() != 1:
            return 0
        subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state" , "off"])
        return 1
        