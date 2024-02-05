import os

USERPROFILE = os.getenv("USERPROFILE")
STARTUP_PATH = f"{USERPROFILE}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
SYSTEMROOT = os.getenv("SYSTEMROOT")
SYSTEM_32 = os.path.join(SYSTEMROOT, "System32")
TEMP = os.getenv("temp")
CMD_PATH = f"{SYSTEM_32}\\cmd.exe"
POWERSHELL_PATH = f"{SYSTEM_32}\\WindowsPowerShell\\v1.0\\powershell.exe"
WSCRIPT_PATH = f"{SYSTEM_32}\\wscript.exe"
HOSTS_PATH = f"{SYSTEM_32}\\drivers\\etc\\hosts"
THEMES_PATH = f"{USERPROFILE}\\AppData\\Roaming\\Microsoft\\Windows\\Themes"