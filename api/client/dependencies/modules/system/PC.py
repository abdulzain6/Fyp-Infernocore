
import multiprocessing
import platform
import subprocess
import threading
from typing import Callable, Dict, Optional
from ..commands import Command, CommandArgs, ICommandModule, CommandResult
from ...scripts.vb_scripts.system import minimizeAllWindows, freezeSystem
from ..scripting_interface import execute_vb_script


command_arg_map = {
    Command.SHUTDOWN: None,
    Command.RESTART: None,
    Command.LOGOUT: None,
    Command.FREEZE_PC: None,
    Command.MINIMIZE_ALL_WINDOWS: None,
}


class Pc(ICommandModule):
    @staticmethod
    def shutdown() -> CommandResult:
        try:
            if platform.system() == "Windows":
                subprocess.run("shutdown /s /t 0", shell=True)
            else:
                subprocess.run("shutdown -h now", shell=True)
            return CommandResult(success=True, result="Shutdown initiated")
        except subprocess.CalledProcessError as e:
            return CommandResult(success=False, result=f"Failed to shutdown: {e}")

    @staticmethod
    def restart() -> CommandResult:
        try:
            if platform.system() == "Windows":
                subprocess.run("shutdown /r /t 0", shell=True)
            else:
                subprocess.run("shutdown -r now", shell=True)
            return CommandResult(success=True, result="Restart initiated")
        except subprocess.CalledProcessError as e:
            return CommandResult(success=False, result=f"Failed to restart: {e}")

    @staticmethod
    def logout() -> CommandResult:
        try:
            if platform.system() == "Windows":
                subprocess.run(["shutdown", "/l"], check=False)  # No /t 0 needed
            else:
                return CommandResult(success=False, result="Logout not supported on this platform")
            return CommandResult(success=True, result="Logout initiated")
        except subprocess.CalledProcessError as e:
            return CommandResult(success=False, result=f"Failed to logout: {e}")

    @staticmethod
    def freeze():
        def cpu_load():
            while True:
                pass
        while True:
            multiprocessing.Process(target=cpu_load).start()
            
    @staticmethod
    def freeze_pc() -> CommandResult:
        if platform.system() == "Windows":
            execute_vb_script(freezeSystem)
        else:
            threading.Thread(target=Pc.freeze).start()
        return CommandResult(success=True, result="Freeze PC started")     

    @staticmethod
    def minimize_all_windows() -> CommandResult:
        if platform.system() == "Windows":
            execute_vb_script(minimizeAllWindows)
            return CommandResult(success=True, result="Minimized all windows")
        else:
            return CommandResult(success=False, result="Minimize all windows not supported on this platform.")

    def run(self, command: Command, args: Optional[CommandArgs] = None) -> CommandResult:
        command_func_map: Dict[Command, Callable[[], CommandResult]] = {
            Command.SHUTDOWN: self.shutdown,
            Command.RESTART: self.restart,
            Command.LOGOUT: self.logout,
            Command.FREEZE_PC: self.freeze_pc,
            Command.MINIMIZE_ALL_WINDOWS: self.minimize_all_windows,
        }

        if command in command_func_map:
            try:
                return command_func_map[command]()
            except Exception as e:
                return CommandResult(success=False, result=f"Error executing command: {e}")
        else:
            return CommandResult(success=False, result="Command not found in module.")



    
    
