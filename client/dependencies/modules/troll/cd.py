import ctypes
import platform
import time, threading
from pydantic import BaseModel
from ..commands import Command, ICommandModule, CommandResult, CommandArgs
from typing import Optional



class EjectCdArgs(CommandArgs):
    delay: Optional[int] = 1

command_arg_map = {
    Command.EJECT_CD: None,
    Command.EJECT_CD_CONTINOUS: None,
    Command.STOP_CD_EJECTOR: EjectCdArgs,
}

class Cd(ICommandModule):
    def __init__(self):
        self.eject = False
        self.eject_thread: Optional[threading.Thread] = None
    
    @staticmethod
    def eject_once() -> CommandResult:
        try:
            ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
            return CommandResult(result="CD drive door opened once.", success=True)
        except Exception as e:
            return CommandResult(result=str(e), success=False)
    
    def eject_continuous(self, args: EjectCdArgs) -> CommandResult:
        if not self.eject:
            self.eject = True
            self.eject_thread = threading.Thread(target=self._eject_continuous_helper, args=(args.delay,))
            self.eject_thread.start()
            return CommandResult(result="CD drive door eject continuous started.", success=True)
        else:
            return CommandResult(result="Ejector is already running.", success=False)

    def _eject_continuous_helper(self, delay):
        while self.eject:
            ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
            time.sleep(delay)

    def stop_eject(self) -> CommandResult:
        if self.eject:
            self.eject = False
            if self.eject_thread:
                self.eject_thread.join()
            return CommandResult(result="CD drive door eject continuous stopped.", success=True)
        else:
            return CommandResult(result="Ejector was not running.", success=False)

    def run(self, command: Command, args: Optional[BaseModel] = None) -> CommandResult:
        command_map = {
            Command.EJECT_CD: lambda: self.eject_once(),
            Command.EJECT_CD_CONTINOUS: lambda: self.eject_continuous(
                EjectCdArgs.model_validate(args.model_dump())
            ),
            Command.STOP_CD_EJECTOR: lambda: self.stop_eject(),
        }
        if platform.system() != "Windows":
            return CommandResult(success=False, result="This command is supported on Windows only.")

        if command in command_map:
            try:
                return command_map[command]()
            except Exception as e:
                return CommandResult(result=f"Error executing command: {e}", success=False)
        else:
            return CommandResult(result="Command not found in module.", success=False)
