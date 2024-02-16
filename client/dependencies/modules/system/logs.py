import os
import shutil
import ctypes
import platform
from typing import Callable, Dict, Optional

from pydantic import ValidationError
from ..constants import LOGS_PATH
from ..commands import Command, CommandArgs, ICommandModule, CommandResult


def is_elevated():
    if platform.system() == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return os.geteuid() == 0
    
command_arg_map = {
    Command.GET_LOGS: None,
    Command.CLEAR_LOGS: None
}
    
class Logs(ICommandModule):
    @staticmethod
    def get_logs() -> CommandResult:
        if not LOGS_PATH or not os.path.exists(LOGS_PATH):
            return CommandResult(success=False, result="Log path does not exist or is not defined for this platform.")
        try:
            logs = [log for log in os.listdir(LOGS_PATH) if os.path.isfile(os.path.join(LOGS_PATH, log))]
            return CommandResult(success=True, result=logs)
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    @staticmethod
    def clear_logs() -> CommandResult:
        if not is_elevated():
            return CommandResult(success=False, result="Elevated privileges required.")
        if not LOGS_PATH or not os.path.exists(LOGS_PATH):
            return CommandResult(success=False, result="Log path does not exist or is not defined for this platform.")
        try:
            for log in os.listdir(LOGS_PATH):
                log_path = os.path.join(LOGS_PATH, log)
                if os.path.isfile(log_path):
                    os.remove(log_path)
                else:
                    shutil.rmtree(log_path, ignore_errors=True)
            return CommandResult(success=True, result="Logs cleared successfully.")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def run(self, command: Command, args: Optional[CommandArgs] = None) -> CommandResult:
        command_func_map: Dict[Command, Callable[[Optional[CommandArgs]], CommandResult]] = {
            Command.GET_LOGS: lambda args: self.get_logs(),
            Command.CLEAR_LOGS: lambda args: self.clear_logs(),
        }
        if command not in command_func_map:
            return CommandResult(success=False, result="Error: Command not found in module.")
        try:
            return command_func_map[command](args)
        except ValidationError as e:
            return CommandResult(success=False, result=f"Validation error: {e}")
        except Exception as e:
            return CommandResult(success=False, result=f"Error: {e}")
