import ctypes
import os
import platform
import socket
import subprocess
from typing import Callable, Dict

import psutil
from ..commands import Command, CommandArgs, ICommandModule, CommandResult


command_arg_map = {
    Command.DISABLE_INTERNET: None,
    Command.ENABLE_INTERNET: None,
}

class Internet(ICommandModule):
    def __init__(self) -> None:
        active_interface = Internet.get_active_interface()
        
    @staticmethod
    def is_elevated() -> bool:
        if platform.system() == "Windows":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return False
        else:
            return os.geteuid() == 0

    def disable_internet(self) -> CommandResult:
        try:
            if platform.system() == "Windows":
                subprocess.run(["ipconfig", "/release"], check=True)
            elif platform.system() in ["Linux", "Darwin"]:  # Darwin is macOS
                if not Internet.is_elevated():
                    return CommandResult(success=False, result="Elevated privileges are required.")
                subprocess.run(["ifconfig", self.active_interface, "down"], check=True)
            return CommandResult(success=True, result="Internet disabled.")
        except Exception as e:
            return CommandResult(success=False, result=f"Error disabling internet: {str(e)}")

    def enable_internet(self) -> CommandResult:
        try:
            if platform.system() == "Windows":
                subprocess.run(["ipconfig", "/renew"], check=True)
            elif platform.system() in ["Linux", "Darwin"]:
                if not Internet.is_elevated():
                    return CommandResult(success=False, result="Elevated privileges are required.")
                subprocess.run(["ifconfig", self.get_active_interface(), "up"], check=True)
            return CommandResult(success=True, result="Internet enabled.")
        except Exception as e:
            return CommandResult(success=False, result=f"Error enabling internet: {str(e)}")

    @staticmethod
    def get_active_interface() -> str:
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        
        # Iterate through interfaces, looking for the first that is up and has an IPv4 address
        for interface, addrs in interfaces.items():
            if interface != "lo" and stats[interface].isup:  # Ignore loopback and down interfaces
                for addr in addrs:
                    if addr.family == socket.AF_INET:  # IPv4
                        return interface  # Return the first match
                
        return ""  # Return an empty string if no suitable interface is found

    def run(self, command: Command, args: CommandArgs = None) -> CommandResult:
        command_func_map: Dict[Command, Callable[[], CommandResult]] = {
            Command.DISABLE_INTERNET: self.disable_internet,
            Command.ENABLE_INTERNET: self.enable_internet,
        }

        if command in command_func_map:
            try:
                return command_func_map[command]()
            except Exception as e:
                return CommandResult(success=False, result=f"Error executing {command}: {str(e)}")
        else:
            return CommandResult(success=False, result="Command not found in module.")
