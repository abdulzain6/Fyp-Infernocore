import ctypes, platform
from ctypes import wintypes
import random
import threading
from ..commands import Command, CommandResult, ICommandModule

command_arg_map = {
    Command.START_WINDOW_TROLL: None,
    Command.STOP_WINDOW_TROLL: None
}

class WindowTroll(ICommandModule):
    def __init__(self) -> None:
        if platform.system() == "Windows":
            self.user32 = ctypes.windll.user32
            self.EnumWindows = self.user32.EnumWindows
            self.EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
            self.IsWindowVisible = self.user32.IsWindowVisible
            self.SetWindowPos = ctypes.WinDLL('user32').SetWindowPos
            self.GetForegroundWindow = ctypes.WinDLL('user32').GetForegroundWindow
            self.GetWindowRect = ctypes.WinDLL('user32').GetWindowRect
            self.ShowWindow = ctypes.WinDLL('user32').ShowWindow
            self.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.UINT]
            self.stop = False

            self.screensize = self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1) 
        self.hwnds = []
        self.threads = []

    def get_random_spot(self):
        x = random.randrange(0, self.screensize[0])
        y = random.randrange(0, self.screensize[1])
        return x, y

    def move_window(self, hwnd):
        while not self.stop:
            x_target, y_target = self.get_random_spot()
            rect = wintypes.RECT()
            self.GetWindowRect(hwnd, ctypes.pointer(rect))
            y_origin, x_origin = rect.left, rect.top
            diff = ((x_target - x_origin) // 100, (y_target - y_origin) // 100)
            self.ShowWindow(hwnd, 9)
            for _ in range(100):
                x_origin += diff[0]
                y_origin += diff[1]
                self.SetWindowPos(hwnd, None, x_origin, y_origin, 0, 0, 0x0040)

    def get_windows(self):
        def foreach_window(hwnd, lParam):
            if self.IsWindowVisible(hwnd) and hwnd not in self.hwnds:
                self.hwnds.append(hwnd)
            return True
        self.EnumWindows(self.EnumWindowsProc(foreach_window), 0)

    def start_troll(self) -> CommandResult:
        self.stop = False
        self.get_windows()
        for hwnd in self.hwnds:
            t = threading.Thread(target=self.move_window, args=(hwnd,))
            t.start()
            self.threads.append(t)
        return CommandResult(success=True, result="Window trolling started.")

    def stop_troll(self) -> CommandResult:
        self.stop = True
        for thread in self.threads:
            thread.join()
        self.threads.clear()
        return CommandResult(success=True, result="Window trolling stopped.")

    def run(self, command: Command, args=None) -> CommandResult:
        if platform.system() != "Windows":
            return CommandResult(success=False, result="This command is supported on Windows only.")

        if command == Command.START_WINDOW_TROLL:
            return self.start_troll()
        elif command == Command.STOP_WINDOW_TROLL:
            return self.stop_troll()
        else:
            return CommandResult(success=False, result="Invalid command.")
