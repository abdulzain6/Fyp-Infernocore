import ctypes
from ctypes import wintypes
import random
import threading

class window_troll:
    def __init__(self) -> None:
        user32 = ctypes.windll.user32
        self.EnumWindows = ctypes.windll.user32.EnumWindows
        self.EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        self.IsWindowVisible = ctypes.windll.user32.IsWindowVisible
        self.SetWindowPos = ctypes.WinDLL('user32').SetWindowPos
        self.GetForegroundWindow = ctypes.WinDLL('user32').GetForegroundWindow
        self.GetWindowRect = ctypes.WinDLL('user32').GetWindowRect
        self.ShowWindow = ctypes.WinDLL('user32').ShowWindow
        self.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.UINT]
        self.SetWindowPos.restype = wintypes.BOOL 
        self.stop = False

        self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) 
        self.hwnds = []
        

 
    def get_random_spot(self):
        x = random.randrange(0, self.screensize[0])
        y = random.randrange(0, self.screensize[1])
        return x , y
    

    def move_window(self, hwnd):
        while not self.stop:
            x_target, y_target = self.get_random_spot()
            rect = wintypes.RECT()
            self.GetWindowRect(hwnd, ctypes.pointer(rect))
            
            y_origin = rect.left
            x_origin = rect.top

            diff = (x_target + x_origin) // 100 , (y_target + y_origin) // 100

            self.ShowWindow(hwnd, 9)
            for _ in range(100):
                x_origin = abs(x_origin + diff[0]) % self.screensize[0]
                y_origin = abs(y_origin + diff[1]) % self.screensize[1]
                self.SetWindowPos(hwnd, None, x_origin, y_origin, 100, 100, 0x0040)

    def get_windows(self):
        def foreach_window(hwnd, lParam):
            if self.IsWindowVisible(hwnd) and hwnd not in self.hwnds:
                self.hwnds.append(hwnd)
            return True

        self.EnumWindows(self.EnumWindowsProc(foreach_window), 0)

    def start(self):
        self.get_windows()
        for hwnd in self.hwnds:
            t = threading.Thread(target=self.move_window, args=(hwnd,))
            t.start()       


    def stop_troll(self):
        self.stop = True
            
    
window_troll_obj = window_troll()