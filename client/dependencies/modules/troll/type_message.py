import platform
import subprocess, time, pyautogui, multiprocessing

from typing import Optional
from pydantic import BaseModel, Field

from ..scripting_interface import execute_vb_script
from ..input_output.block_input import BlockInput, BlockDurationArgs
from ...scripts.vb_scripts.system import minimizeAllWindows
from ..commands import Command, CommandResult, CommandArgs, ICommandModule


class TypeMessageArgs(CommandArgs):
    message: str
    blocktime: int
    delayChar: float = Field(default=0.05, description="Delay between each character typing")

command_arg_map = {
    Command.TYPE_MESSAGE_NOTEPAD: TypeMessageArgs,
}

class TypeMessage(ICommandModule):
    def __init__(self, block_input: BlockInput) -> None:
        self.block_input = block_input

    def _type(self, message, delayChar: int):
        subprocess.Popen(["C:\\Windows\\notepad.exe"])
        time.sleep(2)
        pyautogui.write(message, interval=delayChar)

    def minimize_all_windows(self) -> CommandResult:
        if platform.system() == "Windows":
            execute_vb_script(minimizeAllWindows)
            return CommandResult(result="All windows minimized.", success=True)
        else:
            return CommandResult(result="This feature is supported on Windows only.", success=False)

    def type_message_notepad(self, args: TypeMessageArgs) -> CommandResult:
        try:
            self.minimize_all_windows()
            th = multiprocessing.Process(target=self._type, args=(args.message, args.delayChar))
            th.start()
            self.block_input.block_secs(BlockDurationArgs(seconds=args.blocktime))
            return CommandResult(result="Message typing started.", success=True)
        except Exception as e:
            return CommandResult(result=str(e), success=False)

    def run(self, command: Command, args: Optional[BaseModel] = None) -> CommandResult:
        command_map = {
            Command.TYPE_MESSAGE_NOTEPAD: lambda: self.type_message_notepad(
                TypeMessageArgs.model_validate(args.model_dump())
            ),
        }
        if platform.system() != "Windows":
            return CommandResult(result="This feature is supported on Windows only.", success=False)

        if command in command_map:
            try:
                if args is None and command != Command.MINIMIZE_ALL_WINDOWS:
                    return CommandResult(success=False, result="No Args passed")
                return command_map[command]()
            except Exception as e:
                return CommandResult(success=False, result=f"Error: {e}")
        else:
            return CommandResult(success=False, result="Command not found in module.")
 