import ctypes, time, threading
from ctypes import wintypes
from ...scripts.vb_scripts.system import minimizeAllWindows as mav
from ..scripting_interface import execute_vb_script

class Window:
    def __init__(self) -> None:
        self.GetForegroundWindow = ctypes.WinDLL('user32').GetForegroundWindow
        self.EnableWindow = ctypes.WinDLL('user32').EnableWindow 
        self.EnableWindow.argtypes = [ctypes.c_void_p, wintypes.BOOL]
        self.EnableWindow.restype = wintypes.BOOL
        self.handles = set()
        self.disable = False
    
    def disable_current_window(self):
        h = self.GetForegroundWindow()
        return self.EnableWindow(h, False)
         
    
    def enable_current_window(self):
        h = self.GetForegroundWindow()
        return self.EnableWindow(h, True)
    
    def __disabler (self):
        while self.disable:
            h = self.GetForegroundWindow()
            self.EnableWindow(h, False)
            self.handles.add(h)
            time.sleep(1)

    def disable_current_windows_continous(self):
        self.disable = True
        t = threading.Thread(target = self.__disabler)
        t.start()

    def stop_disabler(self):
        self.disable = False
        for i in self.handles:
            self.EnableWindow(i, True)

    @staticmethod
    def get_foreground_window_title():
        _GetWindowText = ctypes.WinDLL('user32').GetWindowTextW
        _GetWindowText.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int]
        _GetWindowText.restype = ctypes.c_int
        GetForegroundWindow = ctypes.WinDLL('user32').GetForegroundWindow
        h = GetForegroundWindow()
        b = ctypes.create_unicode_buffer(300)
        _GetWindowText(h, b, 300)
        return b.value
        
def minimize_all_windows():
    execute_vb_script(mav)


window_obj = Window()




