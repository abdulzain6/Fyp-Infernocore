import winreg
import processManagement


class CMD:
    def __init__(self) -> None:
        if processManagement.isElevated() == 1:
            sub_key = "SOFTWARE\\Policies\\Microsoft\\Windows\\System"
            self.h = winreg.CreateKeyEx(
                winreg.HKEY_CURRENT_USER, sub_key, reserved = 0, access = winreg.KEY_ALL_ACCESS)

    def enable(self):
        return self.change_dword(0)

    def disable(self):
        return self.change_dword(1)
    
    def disable_fully(self):
        return self.change_dword(2)

    def change_dword(self, arg0):
        if processManagement.isElevated() != 1:
            return 0
        winreg.SetValueEx(self.h, "DisableCMD", 0, winreg.REG_DWORD, arg0)
        return 1

cmd_obj = CMD()