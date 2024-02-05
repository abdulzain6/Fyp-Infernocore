import subprocess, os
from ..constants import SYSTEM_32
from ...scripts.vb_scripts.system import minimizeAllWindows, freezeSystem
from ..scripting_interface import execute_vb_script


class Pc:
    @staticmethod
    def shutdown():
        subprocess.run([os.path.join(SYSTEM_32, "shutdown"), "/s", "/t", "0"])

    @staticmethod
    def restart():
        subprocess.run([os.path.join(SYSTEM_32, "shutdown"), "/r", "/t", "0"])

    @staticmethod
    def logout():
        subprocess.run([os.path.join(SYSTEM_32, "shutdown"), "/l", "/t", "0"])

    @staticmethod
    def freeze_pc():
        execute_vb_script(freezeSystem)
    
    @staticmethod
    def minimize_all_windows():
        execute_vb_script(minimizeAllWindows)





    
    
