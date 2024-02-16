import subprocess
import platform
import ctypes, os
from ..commands import Command, CommandArgs, ICommandModule, CommandResult

command_arg_map = {
    Command.FIREWALL_OFF: None,
    Command.FIREWALL_ON: None,
}

class Firewall(ICommandModule):
    @staticmethod
    def is_elevated() -> bool:
        if platform.system() == "Windows":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return False
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            return os.geteuid() == 0
        return False

    @staticmethod
    def firewall_on() -> CommandResult:
        if not Firewall.is_elevated():
            return CommandResult(success=False, result="Elevated privileges are required.")
        
        if platform.system() == "Windows":
            subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "on"], check=True)
            return CommandResult(success=True, result="Firewall enabled.")
        else:
            return CommandResult(success=False, result="Firewall management is not supported on this platform through this method.")

    @staticmethod
    def firewall_off() -> CommandResult:
        if not Firewall.is_elevated():
            return CommandResult(success=False, result="Elevated privileges are required.")
        
        if platform.system() == "Windows":
            subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "off"], check=True)
            return CommandResult(success=True, result="Firewall disabled.")
        else:
            return CommandResult(success=False, result="Firewall management is not supported on this platform through this method.")

    def run(self, command: Command, args: CommandArgs = None) -> CommandResult:
        command_func_map = {
            Command.FIREWALL_ON: self.firewall_on,
            Command.FIREWALL_OFF: self.firewall_off,
        }

        if command in command_func_map:
            try:
                return command_func_map[command]()
            except Exception as e:
                return CommandResult(success=False, result=f"Error executing {command}: {str(e)}")
        else:
            return CommandResult(success=False, result="Command not found in module.")
