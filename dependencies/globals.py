from .modules.file_system import FileSystem
from .modules.commands import Command, CommandArgs, command_to_module_map, ICommandModule, CommandResult

filesystem_handler = FileSystem()

def module_factory(module_name: str) -> ICommandModule:
    module_name_map = {"file_system" : filesystem_handler}
    if module_name not in module_name_map:
        raise ValueError("Module Not found")
    return module_name_map[module_name]


def command_executor(command: Command, args: CommandArgs) -> CommandResult:
    module = module_factory(command_to_module_map[command])
    return module.run(command, args)