import subprocess, os
import multiprocessing

from random import randrange
from io import StringIO
from contextlib import redirect_stdout
from typing import Optional
from pydantic import BaseModel
from .constants import *
from .commands import Command, ICommandModule, CommandResult

def execute_powershell_script(
    script: str,
    get_output: str = False,
    timeout: int = 10
):
    if get_output:
        return (
            subprocess.check_output([POWERSHELL_PATH, script], timeout=timeout)
            .decode('utf-8', errors = 'ignore')
            .strip()
        )

    p = subprocess.Popen([POWERSHELL_PATH , script])

def execute_vb_script(script, wait = False):
    fname = f'{os.path.join(TEMP, str(randrange(1, 500000)))}.vbs'
    with open(fname, "w") as file:
        file.write(script)
    p = subprocess.Popen([WSCRIPT_PATH , fname], subprocess.CREATE_NEW_CONSOLE)
    if wait:
        p.wait()

def execute_batch_script(script, getOutput = False, wait = False, createNewConsole = True):
    fname = f'{os.path.join(TEMP, str(randrange(1, 500000)))}.bat'
    with open(fname, "w") as file:
        file.write(script)

    if getOutput:
        return subprocess.check_output([CMD_PATH, "/c", fname]).decode('utf-8', errors = 'ignore').strip()

    if createNewConsole:
        p = subprocess.Popen([CMD_PATH, "/c", "start", fname] , subprocess.CREATE_NEW_CONSOLE)
    else:
        p = subprocess.Popen([CMD_PATH, "/c", "start", fname])

    if wait:
        p.wait()

def execute_python_script(script: str, timeout: int = 10) -> str:
    def script_runner(script: str, output: multiprocessing.Queue):
        f = StringIO()
        with redirect_stdout(f):
            try:
                exec(script)
            except Exception as e:
                output.put(str(e))
                return
        output.put(f.getvalue())

    output = multiprocessing.Queue()
    process = multiprocessing.Process(target=script_runner, args=(script, output))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        return "Script execution timed out"

    result = output.get() if not output.empty() else "No output"
    return result


class RunPythonArgs(BaseModel):
    script: str
    timeout: int = 10

class RunPowershellArgs(RunPythonArgs):
    get_output: bool = True
    
command_arg_map = {
    Command.RUN_POWERSHELL_SCRIPT: RunPowershellArgs,
    Command.RUN_PYTHON_SCRIPT: RunPythonArgs,
}

class Scripting(ICommandModule):  
    @staticmethod
    def run_python_script(args: RunPythonArgs) -> CommandResult:
        try:
            result = execute_python_script(args.script, args.timeout)
            return CommandResult(result=result, success=True)
        except Exception as e:
            return CommandResult(result=str(e), success=False)

    @staticmethod
    def run_powershell_script(args: RunPowershellArgs) -> CommandResult:
        try:
            result = execute_powershell_script(args.script, args.get_output, args.timeout)
            return CommandResult(result=result, success=True)
        except Exception as e:
            return CommandResult(result=str(e), success=False)

    def run(self, command: Command, args: Optional[BaseModel] = None) -> CommandResult:
        command_map = {
            Command.RUN_POWERSHELL_SCRIPT: lambda: self.run_powershell_script(
                RunPowershellArgs.model_validate(args.model_dump())
            ),
            Command.RUN_PYTHON_SCRIPT: lambda: self.run_python_script(
                RunPythonArgs.model_validate(args.model_dump())
            ),
        }
        if command in command_map:
            try:
                return command_map[command]()
            except Exception as e:
                return CommandResult(result=f"Error executing command: {e}", success=False)
        else:
            return CommandResult(result="Command not found in module.", success=False)

