import ctypes
import os
import platform
import subprocess
from typing import Callable, Dict, Optional
import psutil
from pydantic import ValidationError
from ..commands import Command, CommandArgs, ICommandModule, CommandResult

class CreateAccountArgs(CommandArgs):
    name: str
    password: str
    full_name: Optional[str] = None
    description: Optional[str] = None
    
command_arg_map = {
    Command.CREATE_ACCOUNT: CreateAccountArgs,
    Command.GET_ACCOUNTS: None,
}
    
class AccountManager(ICommandModule):
    def is_admin(self):
        if platform.system() == "Windows":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
        else:
            return os.geteuid() == 0

    def get_accounts(self) -> CommandResult:
        users = psutil.users()
        unique_users = {user.name: {'Name': user.name, 'Host': user.host, 'Started': user.started} for user in users}.values()
        accounts = [{'id': i+1, **user} for i, user in enumerate(unique_users)]
        return CommandResult(success=True, result=accounts)

    def create_account(self, args: CreateAccountArgs) -> CommandResult:
        if not self.is_admin():
            return CommandResult(result="This action requires administrative privileges.", success=False)
        
        if platform.system() == "Windows":
            command = f"net user {args.name} {args.password} /ADD"
            if args.full_name:
                command += f" /FULLNAME:\"{args.full_name}\""
            if args.description:
                command += f" /COMMENT:\"{args.description}\""
        elif platform.system() == "Linux":
            # Note: Consider using `chpasswd` for setting password due to security concerns
            command = f"useradd -m {args.name} && echo {args.name}:{args.password} | chpasswd"
            if args.full_name:
                command += f" -c \"{args.full_name}\""
        else:
            return CommandResult(result="Unsupported platform", success=False)
        
        try:
            subprocess.check_call(command, shell=True)
            return CommandResult(result="User created successfully", success=True)
        except subprocess.CalledProcessError as e:
            return CommandResult(result=f"Failed to create user: {e}", success=False)

    def run(self, command: Command, args: CommandArgs = None) -> CommandResult:
        print(f"AccountManager module handling {command} with {args}")
        
        command_func_map_with_args: Dict[Command, Callable[[CommandArgs], CommandResult]] = {
            Command.CREATE_ACCOUNT: self.create_account,
        }
        
        command_func_map_no_args: Dict[Command, Callable[[], CommandResult]] = {
            Command.GET_ACCOUNTS: self.get_accounts,
        }
        
        if command not in command_func_map_no_args and command not in command_func_map_with_args:
            return CommandResult(result=f"Error: Command not found in module.", success=False)
        
        try:
            if command in command_func_map_no_args:
                print("Executing command with no args")
                return command_func_map_no_args[command]()
            else:
                print(f"Executing command with {args}")
                if args is None:
                    return CommandResult(success=False, result="No Args passed")
                validated_args = command_arg_map[command](**args.model_dump())
                return command_func_map_with_args[command](validated_args)
        except ValidationError as e:
            return CommandResult(success=False, result=f"Validation error: {e}")
        except Exception as e:
            return CommandResult(success=False, result=f"Error: {e}")