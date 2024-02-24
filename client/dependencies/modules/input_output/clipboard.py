import threading
import time
from typing import Optional
from pyperclip import copy, paste
from ..commands import Command, CommandArgs, ICommandModule, CommandResult



class ClipboardFillerArgs(CommandArgs):
    text: str

class ClipboardCommandArgs(ClipboardFillerArgs):
    pass

command_arg_map = {
    Command.GET_CLIPBOARD: None,
    Command.FILLER_OFF: None,
    Command.GET_CLIPBOARD_FILLER_STATUS: None,
    Command.PASTE_TO_CLIPBOARD: ClipboardCommandArgs,
    Command.CLIPBOARD_FILLER: ClipboardFillerArgs
}

class Clipboard(ICommandModule):
    def __init__(self, sleep: float = 0.2):
        self.isClipboardFillerOn = False
        self.sleep = sleep
        self.filler_thread: Optional[threading.Thread] = None

    def copy_text(self, args: ClipboardCommandArgs) -> CommandResult:
        if args.text is not None:
            copy(args.text)
            return CommandResult(success=True, result="Text copied to clipboard.")
        return CommandResult(success=False, result="No text provided.")

    def get_text(self) -> CommandResult:
        text = paste()
        return CommandResult(success=True, result=text)

    def clipboard_filler(self, text: str):
        while self.isClipboardFillerOn:
            copy(text)
            time.sleep(self.sleep)

    def start_filler(self, args: ClipboardFillerArgs) -> CommandResult:
        if not self.isClipboardFillerOn:
            self.isClipboardFillerOn = True
            self.filler_thread = threading.Thread(target=self.clipboard_filler, args=(args.text,))
            self.filler_thread.start()
            return CommandResult(success=True, result="Clipboard filler started.")
        return CommandResult(success=False, result="Clipboard filler is already running.")

    def stop_filler(self) -> CommandResult:
        if self.isClipboardFillerOn:
            self.isClipboardFillerOn = False
            if self.filler_thread:
                self.filler_thread.join()
            return CommandResult(success=True, result="Clipboard filler stopped.")
        return CommandResult(success=False, result="Clipboard filler is not running.")

    def get_filler_status(self) -> CommandResult:
        status = "on" if self.isClipboardFillerOn else "off"
        return CommandResult(success=True, result={"status" : status})

    def run(self, command: Command, args: Optional[CommandArgs] = None) -> CommandResult:
        command_func_map = {
            Command.PASTE_TO_CLIPBOARD: self.copy_text,
            Command.CLIPBOARD_FILLER: self.start_filler
        }
        command_func_map_no_args = {
            Command.GET_CLIPBOARD: self.get_text,
            Command.FILLER_OFF: self.stop_filler,
            Command.GET_CLIPBOARD_FILLER_STATUS: self.get_filler_status,
        }

        if command in command_func_map or command in command_func_map_no_args:
            try:
                if command in command_func_map:
                    if not args:
                        return CommandResult(success=False, result="No Args passed")
                    return command_func_map.get(command)(args)
                else:
                    return command_func_map_no_args.get(command)()
            except Exception as e:
                return CommandResult(success=False, result=f"Error: {e}")
        else:
            return CommandResult(success=False, result="Command not found in module.")
