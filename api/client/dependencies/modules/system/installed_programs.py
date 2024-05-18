import os
import platform
try:
    import winreg
except Exception:
    winreg = None
from typing import Callable, Dict, Optional
from ..scripting_interface import execute_batch_script
from pydantic import ValidationError, BaseModel
from ..commands import Command, CommandArgs, ICommandModule, CommandResult



class Program(BaseModel):
    id: str | int
    name: str
    uninstall_string: str
    publisher: str
    version: str

class UninstallArgs(CommandArgs):
    uninstall_string: str

command_arg_map = {
    Command.RUN_UNINSTALLER: UninstallArgs, 
    Command.GET_INSTALLED_PROGRAMS: None
}

class Programs(ICommandModule):
    def get_installed_programs(self) -> CommandResult:
        try:
            if platform.system() == "Windows":
                hkey = winreg.OpenKeyEx(
                    winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", reserved=0, access=winreg.KEY_READ)
                keys = self._enum_keys(hkey)
                key_data = self._get_info_from_keys(
                    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", keys)
                
                programs: list[Program] = []
                i = 0
                for data in key_data:
                    try:
                        i += 1
                        programs.append(Program(id=i, name=data["DisplayName"][0], uninstall_string=data["UninstallString"]
                                        [0], publisher=data["Publisher"][0], version=data["DisplayVersion"][0]))
                    except KeyError:
                        pass
                    
                return CommandResult(result=[program.model_dump() for program in programs], success=True)
            else:
                return CommandResult(result="Not supported on linux", success=False)
        except Exception as e:
            return CommandResult(result=f"Error: {e}", success=False)

    def run_uninstaller(self, args: UninstallArgs) -> CommandResult:
        try:
            if "MsiExec.exe" in args.uninstall_string:
                execute_batch_script(
                    f'{args.uninstall_string} /quiet',
                    getOutput=True,
                )
            else:
                execute_batch_script(args.uninstall_string, getOutput=True)
                
            return CommandResult(result=f"Uninstall Success!", success=True)
        except Exception as e:
            return CommandResult(result=f"Error: {e}", success=False)

    def _enum_keys(self, hkey):
        keys = []
        i = 0
        while True:
            try:
                keys.append(winreg.EnumKey(hkey, i))
            except OSError:
                break
            i += 1
        return keys

    def _get_values(self, key):
        key_dict = {}
        i = 0
        while True:
            try:
                subvalue = winreg.EnumValue(key, i)
            except WindowsError as e:
                break
            key_dict[subvalue[0]] = subvalue[1:]
            i += 1
        return key_dict

    def _get_info_from_keys(self, path, keys):
        data = []
        for k in keys:
            key_path = ""
            key_path = os.path.join(path, k)
            hkey = winreg.OpenKeyEx(
                winreg.HKEY_LOCAL_MACHINE, key_path, reserved=0, access=winreg.KEY_READ)
            data.append(self._get_values(hkey))
        return data
    
    def run(self, command: Command, args: Optional[CommandArgs] = None) -> CommandResult:
        command_func_map_with_args: Dict[Command, Callable[[CommandArgs], CommandResult]] = {
            Command.RUN_UNINSTALLER: self.run_uninstaller,
        }

        command_func_map_no_args: Dict[Command, Callable[[], CommandResult]] = {
            Command.GET_INSTALLED_PROGRAMS: self.get_installed_programs,
        }

        if command in command_func_map_no_args:
            return command_func_map_no_args[command]()
        elif command in command_func_map_with_args:
            if args is None:
                return CommandResult(success=False, result="No Args passed")
            try:
                return command_func_map_with_args[command](args)
            except ValidationError as e:
                return CommandResult(success=False, result=f"Validation error: {e}")
        else:
            return CommandResult(success=False, result="Error: Command not found in module.")

