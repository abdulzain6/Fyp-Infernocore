import platform
import os

USERPROFILE = os.getenv("USERPROFILE")
STARTUP_PATH = f"{USERPROFILE}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
SYSTEMROOT = os.getenv("SYSTEMROOT", "")
SYSTEM_32 = os.path.join(SYSTEMROOT, "System32")
TEMP = os.getenv("temp", "")
CMD_PATH = f"{SYSTEM_32}\\cmd.exe"
POWERSHELL_PATH = f"{SYSTEM_32}\\WindowsPowerShell\\v1.0\\powershell.exe"
WSCRIPT_PATH = f"{SYSTEM_32}\\wscript.exe"

if platform.system() == "Windows":
    HOSTS_PATH = f"{SYSTEM_32}\\drivers\\etc\\hosts"
    LOGS_PATH = os.path.join(os.environ.get("SYSTEMROOT", "C:\\Windows"), "Logs")
else:
    HOSTS_PATH = "/etc/hosts"
    LOGS_PATH = "/var/log"


THEMES_PATH = f"{USERPROFILE}\\AppData\\Roaming\\Microsoft\\Windows\\Themes"