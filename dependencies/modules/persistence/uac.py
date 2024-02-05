import winreg
import processManagement


class UAC:
    def __init__(self) -> None:
        if processManagement.isElevated() == 1:
            sub_key = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System"
            self.h = winreg.CreateKeyEx(
                winreg.HKEY_LOCAL_MACHINE, sub_key, reserved = 0, access = winreg.KEY_ALL_ACCESS)

    def disable(self):
        return self.change_dword(0)

    def enable(self):
        return self.change_dword(1)

    def change_dword(self, arg0):
        if processManagement.isElevated() != 1:
            return 0
        winreg.SetValueEx(self.h, "EnableLUA", 0, winreg.REG_DWORD, arg0)
        return 1

