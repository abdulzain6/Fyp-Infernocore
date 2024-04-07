import ctypes, time
import threading
import multiprocessing
import platform, os
from pydantic import BaseModel, Field
from typing import Optional
from ...extensions.mouseBlock_code import mouseBlock
from ..commands import Command, CommandArgs, ICommandModule, CommandResult


class BlockDurationArgs(CommandArgs):
    seconds: int = Field(..., gt=0, description="Duration in seconds for which to block input")

command_arg_map = {
    Command.BLOCK: None,
    Command.UNBLOCK: None,
    Command.GET_BLOCK_STATUS: None,
    Command.REVERSE_MOUSE_BUTTONS: None,
    Command.BLOCK_SECS: BlockDurationArgs,
}
class BlockInput(ICommandModule):
    def __init__(self):
        self.is_blocked = False
        self.block_process: Optional[multiprocessing.Process] = None
        self.mouse_buttons_reversed = False

    def reverse_mouse_buttons(self) -> CommandResult:
        """
        Reverses the primary and secondary mouse buttons.
        """
        if self.mouse_buttons_reversed:
            # Restore the mouse button order
            ctypes.windll.user32.SwapMouseButton(False)
            self.mouse_buttons_reversed = False
            return CommandResult(success=True, result="Mouse buttons restored to original order.")
        else:
            # Reverse the mouse button order
            ctypes.windll.user32.SwapMouseButton(True)
            self.mouse_buttons_reversed = True
            return CommandResult(success=True, result="Mouse buttons reversed.")
        
    def get_block_status(self) -> CommandResult:
        """
        Returns the status of the input blocker.
        """
        if self.is_blocked or (self.block_process and self.block_process.is_alive()):
            return CommandResult(success=True, result={"message": "Input is currently blocked.", "blocked" : True})
        else:
            return CommandResult(success=True, result={"message": "Input is not currently blocked.", "blocked" : False})

    def is_elevated(self) -> bool:
        if platform.system() == "Windows":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return False
        else:
            return os.geteuid() == 0

    def block_for_duration_elevated(self, seconds: int):
        ctypes.windll.user32.BlockInput(True)  # Block all input
        time.sleep(seconds)
        ctypes.windll.user32.BlockInput(False)  # Unblock all input

    def block(self):
        if self.is_elevated():
            self.is_blocked = True
            ctypes.windll.user32.BlockInput(True)  # Block all input
            return CommandResult(success=True, result="Input blocked successfully.")
        else:
            if not self.block_process or not self.block_process.is_alive():
                self.block_process = multiprocessing.Process(target=self.continuous_block_non_elevated)
                self.block_process.start()
                return CommandResult(success=True, result="Mouse input blocking started in background.")
            else:
                return CommandResult(success=False, result="Input is already being blocked.")

    def unblock(self):
        if self.is_elevated():
            ctypes.windll.user32.BlockInput(False)  # Unblock all input
            self.is_blocked = False
            return CommandResult(success=True, result="Input unblocked successfully.")
        else:
            if self.block_process and self.block_process.is_alive():
                self.is_blocked = False
                self.block_process.terminate()
                self.block_process.join()
                return CommandResult(success=True, result="Mouse input blocking stopped.")
            else:
                return CommandResult(success=False, result="No input blocking to stop.")

    def block_secs(self, args: BlockDurationArgs):
        if self.is_elevated():
            thread = multiprocessing.Process(target=self.block_for_duration_elevated, args=(args.seconds,))
            thread.start()
            return CommandResult(success=True, result=f"Input will be blocked for {args.seconds} seconds.")
        else:
            multiprocessing.Process(target=mouseBlock.blockMouseSeconds, args=(args.seconds,)).start()
            return CommandResult(success=True, result=f"Mouse input will be blocked for {args.seconds} seconds in a loop.")

    def continuous_block_non_elevated(self, seconds: int = 5):
        """Blocks mouse for 5 seconds in a loop. Adjust as needed."""
        self.is_blocked = True
        try:
            while self.is_blocked:
                mouseBlock.blockMouseSeconds(seconds)
        except Exception as e:
            print(f"Error: {e}")

    def run(self, command: Command, args: Optional[BaseModel] = None) -> CommandResult:
        if platform.system() != "Windows":
            return CommandResult(success=False, result="This command is supported on Windows only.")
        
        command_func_map_with_args = {
            Command.BLOCK_SECS: self.block_secs,
        }

        command_func_map_no_args = {
            Command.BLOCK: self.block,
            Command.UNBLOCK: self.unblock,
            Command.GET_BLOCK_STATUS: self.get_block_status,
            Command.REVERSE_MOUSE_BUTTONS: self.reverse_mouse_buttons,
        }

        if command in command_func_map_no_args:
            return command_func_map_no_args[command]()
        elif command in command_func_map_with_args:
            if not args:
                return CommandResult(success=False, result="No arguments passed for command requiring arguments.")
            return command_func_map_with_args[command](args)
        else:
            return CommandResult(success=False, result="Command not found.")