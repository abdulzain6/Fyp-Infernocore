import os
from subprocess import CalledProcessError
import winreg
from ..scripting_interface import execute_batch_script

class Program:
    def __init__(self, id, name, uninstall_string, publisher, version) -> None:
        self.id = id
        self.name = name
        self.uninstall_string = uninstall_string
        self.publisher = publisher
        self.version = version

    def __repr__(self) -> str:
        return f"[{self.id}, {self.name}, {self.uninstall_string}, {self.publisher}, {self.version}]"


class Programs:

    def _enum_keys(self, hkey):
        keys = []
        i = 0
        while True:
            try:
                keys.append(winreg.EnumKey(hkey, i))
            except OSError:
                break
            i += 1
        return keys

    def _get_values(self, key):
        key_dict = {}
        i = 0
        while True:
            try:
                subvalue = winreg.EnumValue(key, i)
            except WindowsError as e:
                break
            key_dict[subvalue[0]] = subvalue[1:]
            i += 1
        return key_dict

    def _get_info_from_keys(self, path, keys):
        data = []
        for k in keys:
            key_path = ""
            key_path = os.path.join(path, k)
            hkey = winreg.OpenKeyEx(
                winreg.HKEY_LOCAL_MACHINE, key_path, reserved=0, access=winreg.KEY_READ)
            data.append(self._get_values(hkey))
        return data

    def __init__(self) -> None:
        hkey = winreg.OpenKeyEx(
            winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", reserved=0, access=winreg.KEY_READ)
        keys = self._enum_keys(hkey)
        self.data = self._get_info_from_keys(
            "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", keys)

    def get_installed_programs(self):
        self.programs = []
        i = 0
        for data in self.data:
            try:
                i += 1
                self.programs.append(Program(i, data["DisplayName"][0], data["UninstallString"]
                                [0], data["Publisher"][0], data["DisplayVersion"][0]))
            except KeyError:
                pass
        return self.programs

    def run_uninstaller(self, id):
        for program in self.programs:
            if program.id == id:
                try:
                    if "MsiExec.exe" in program.uninstall_string:
                        execute_batch_script(
                            f'{program.uninstall_string} /quiet',
                            getOutput=True,
                        )
                    else:
                        execute_batch_script(program.uninstall_string, getOutput=True)
                except CalledProcessError:
                    pass

                break



programs_obj = Programs()