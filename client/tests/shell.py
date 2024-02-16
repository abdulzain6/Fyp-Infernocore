import subprocess
import os
import shlex
from typing import Dict
import getpass
import socket

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

# Example usage
shell_manager = ShellSessionManager()
session_id = "user1_session"

while True:
    output = shell_manager.execute_command(session_id, input())
    print(output)
