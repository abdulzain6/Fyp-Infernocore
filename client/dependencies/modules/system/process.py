import datetime
from typing import Callable, Dict, Optional, Type
import psutil
from ..commands import Command, CommandArgs, ICommandModule, CommandResult
from pydantic import ValidationError, Field

class KillProcessArgs(CommandArgs):
    pid: int = Field(..., gt=0, description="Process ID to be terminated")

command_arg_map: Dict[Command, Type[CommandArgs]] = {
    Command.KILL_PROCESS: KillProcessArgs,
    Command.GET_PROCESSES: None
}

class ProcessManager(ICommandModule):
    def get_processes() -> CommandResult:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info', 'create_time', 'ppid', 'exe']):
            try:
                start_time = datetime.datetime.fromtimestamp(proc.info['create_time']).strftime('%Y-%m-%d %H:%M:%S') if proc.info['create_time'] else 'N/A'
                process_info = {
                    'name': proc.info['name'],
                    'pid': proc.info['pid'],
                    'username': proc.info['username'],
                    'cpu_usage': f"{proc.info['cpu_percent']}%",
                    'memory_usage': f"{proc.info['memory_info'].rss / (1024 * 1024):.2f} MB",  # RSS memory in MB
                    'start_time': start_time,
                    'parent_pid': proc.info['ppid'],
                    'executable_path': proc.info['exe']
                }
                processes.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return CommandResult(success=True, result=processes)
    
    @staticmethod
    def kill_process(args: KillProcessArgs) -> CommandResult:
        try:
            proc = psutil.Process(args.pid)
            proc.terminate()  # Sends SIGTERM on Unix-like systems, uses TerminateProcess on Windows
            proc.wait(timeout=5)  # Wait for the process to terminate
            return CommandResult(success=True, result=f"Process {args.pid} terminated.")
        except psutil.NoSuchProcess:
            return CommandResult(success=False, result=f"No such process with PID {args.pid}.")
        except psutil.AccessDenied:
            return CommandResult(success=False, result=f"Access denied when trying to terminate PID {args.pid}.")
        except psutil.TimeoutExpired:
            return CommandResult(success=False, result=f"Timeout expired waiting for PID {args.pid} to terminate.")
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    def run(self, command: Command, args: Optional[CommandArgs] = None) -> CommandResult:
        command_func_map_with_args: Dict[Command, Callable[[CommandArgs], CommandResult]] = {
            Command.KILL_PROCESS: ProcessManager.kill_process,
        }

        command_func_map_no_args: Dict[Command, Callable[[], CommandResult]] = {
            Command.GET_PROCESSES: ProcessManager.get_processes,
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
