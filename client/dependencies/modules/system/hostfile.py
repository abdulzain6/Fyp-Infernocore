from pydantic import ValidationError
from typing import Callable, Dict, Optional
from ..constants import HOSTS_PATH
from ..commands import Command, CommandArgs, ICommandModule, CommandResult


class WriteHostfileContentsArgs(CommandArgs):
    data: str
    
command_arg_map = {
    Command.WRITE_HOSTFILE_CONTENTS: WriteHostfileContentsArgs,
    Command.GET_HOSTFILE_CONTENTS: None
}
    
class Hostfile(ICommandModule):
    @staticmethod
    def get_hostfile_contents() -> CommandResult:
        try:
            with open(HOSTS_PATH, "r") as file:
                contents = file.read()
            return CommandResult(success=True, result=contents)
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    @staticmethod
    def write_hostfile_contents(args: WriteHostfileContentsArgs) -> CommandResult:
        try:
            with open(HOSTS_PATH, "w") as file:
                file.write(args.data)
            return CommandResult(success=True, result="Hostfile updated successfully")
        except PermissionError as e:
            return CommandResult(success=False, result="Permission denied: Unable to write to hostfile")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def run(self, command: Command, args: Optional[CommandArgs] = None) -> CommandResult:
        command_func_map_with_args: Dict[Command, Callable[[CommandArgs], CommandResult]] = {
            Command.WRITE_HOSTFILE_CONTENTS: self.write_hostfile_contents,
        }

        command_func_map_no_args: Dict[Command, Callable[[], CommandResult]] = {
            Command.GET_HOSTFILE_CONTENTS: self.get_hostfile_contents,
        }

        if command in command_func_map_no_args:
            return command_func_map_no_args[command]()
        elif command in command_func_map_with_args:
            if args is None:
                return CommandResult(success=False, result="No Args passed")
            try:
                validated_args = command_arg_map[command](**args.model_dump())
                return command_func_map_with_args[command](validated_args)
            except ValidationError as e:
                return CommandResult(success=False, result=f"Validation error: {e}")
        else:
            return CommandResult(success=False, result="Error: Command not found in module.")
