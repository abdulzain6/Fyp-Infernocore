import ctypes
import os
import platform
import threading

from ctypes import *
from ctypes import wintypes as w 


if platform.system() == "Windows":
    def errcheck(result, func, args):
        if result is None or result == 0:
            raise WinError(get_last_error())
        return result

    LRESULT = c_int64
    HCURSOR = c_void_p
    WNDPROC = WINFUNCTYPE(LRESULT, w.HWND, w.UINT, w.WPARAM, w.LPARAM)
    ntdll = ctypes.WinDLL('ntdll.dll')

    # Define the RtlSetProcessIsCritical function
    RtlSetProcessIsCritical = ntdll.RtlSetProcessIsCritical
    RtlSetProcessIsCritical.argtypes = [ctypes.c_bool, ctypes.POINTER(ctypes.c_bool), ctypes.c_bool]
    RtlSetProcessIsCritical.restype = ctypes.c_ulong
    def makeintresourcew(x):
        return w.LPCWSTR(x)

    class WNDCLASSW(Structure):
        _fields_ = [('style', w.UINT), 
                    ('lpfnWndProc', WNDPROC), 
                    ('cbClsExtra', c_int), 
                    ('cbWndExtra', c_int), 
                    ('hInstance', w.HINSTANCE), 
                    ('hIcon', w.HICON), 
                    ('hCursor', HCURSOR), 
                    ('hbrBackground', w.HBRUSH), 
                    ('lpszMenuName', w.LPCWSTR), 
                    ('lpszClassName', w.LPCWSTR)]

    kernel32 = WinDLL('kernel32', use_last_error = True)
    kernel32.GetModuleHandleW.argtypes = w.LPCWSTR, 
    kernel32.GetModuleHandleW.restype = w.HMODULE
    kernel32.GetModuleHandleW.errcheck = errcheck

    user32 = WinDLL('user32', use_last_error = True)
    user32.CreateWindowExW.argtypes = w.DWORD, w.LPCWSTR, w.LPCWSTR, w.DWORD, c_int, c_int, c_int, c_int, w.HWND, w.HMENU, w.HINSTANCE, w.LPVOID
    user32.CreateWindowExW.restype = w.HWND
    user32.CreateWindowExW.errcheck = errcheck
    user32.LoadIconW.argtypes = w.HINSTANCE, w.LPCWSTR
    user32.LoadIconW.restype = w.HICON
    user32.LoadIconW.errcheck = errcheck
    user32.LoadCursorW.argtypes = w.HINSTANCE, w.LPCWSTR
    user32.LoadCursorW.restype = HCURSOR
    user32.LoadCursorW.errcheck = errcheck
    user32.RegisterClassW.argtypes = POINTER(WNDCLASSW), 
    user32.RegisterClassW.restype = w.ATOM
    user32.RegisterClassW.errcheck = errcheck
    user32.ShowWindow.argtypes = w.HWND, c_int
    user32.ShowWindow.restype = w.BOOL
    user32.UpdateWindow.argtypes = w.HWND, 
    user32.UpdateWindow.restype = w.BOOL
    user32.UpdateWindow.errcheck = errcheck
    user32.GetMessageW.argtypes = POINTER(w.MSG), w.HWND, w.UINT, w.UINT
    user32.GetMessageW.restype = w.BOOL
    user32.TranslateMessage.argtypes = POINTER(w.MSG), 
    user32.TranslateMessage.restype = w.BOOL
    user32.DispatchMessageW.argtypes = POINTER(w.MSG), 
    user32.DispatchMessageW.restype = LRESULT
    user32.GetClientRect.argtypes = w.HWND, POINTER(w.RECT)
    user32.GetClientRect.restype = w.BOOL
    user32.GetClientRect.errcheck = errcheck
    user32.DrawTextW.argtypes = w.HDC, w.LPCWSTR, c_int, POINTER(w.RECT), w.UINT
    user32.DrawTextW.restype = c_int
    user32.PostQuitMessage.argtypes = c_int, 
    user32.PostQuitMessage.restype = None
    user32.DefWindowProcW.argtypes = w.HWND, w.UINT, w.WPARAM, w.LPARAM
    user32.DefWindowProcW.restype = LRESULT

    gdi32 = WinDLL('gdi32', use_last_error = True)
    gdi32.GetStockObject.argtypes = c_int, 
    gdi32.GetStockObject.restype = w.HGDIOBJ

    CW_USEDEFAULT = -2147483648
    IDI_APPLICATION = makeintresourcew(32512)
    WS_OVERLAPPEDWINDOW = 13565952
    CS_HREDRAW = 2
    CS_VREDRAW = 1
    IDC_ARROW = makeintresourcew(32512)
    WHITE_BRUSH = 0
    SW_SHOWNORMAL = 1
    WM_PAINT = 15
    WM_DESTROY = 2
    DT_SINGLELINE = 32
    DT_CENTER = 1
    DT_VCENTER = 4
    WM_ENDSESSION = 22




class CriticalProcess:
    def __init__(self) -> None:   
        self.t = threading.Thread(target = self._unprotect_process_end)
        self.t.start()

    def _unprotect_process_end(self):
        def wnd_proc(hwnd, message, wParam, lParam):
            if message == WM_DESTROY:
                user32.PostQuitMessage(0)
                return 0
            elif message == WM_ENDSESSION:
                self.un_protect_process()

            return user32.DefWindowProcW(hwnd, message, wParam, lParam)

        wndclass = WNDCLASSW()
        wndclass.style          = CS_HREDRAW | CS_VREDRAW
        wndclass.lpfnWndProc    = WNDPROC(wnd_proc)
        wndclass.cbClsExtra = wndclass.cbWndExtra = 0
        wndclass.hInstance      = kernel32.GetModuleHandleW(None)
        wndclass.hIcon          = user32.LoadIconW(None, IDI_APPLICATION)
        wndclass.hCursor        = user32.LoadCursorW(None, IDC_ARROW)
        wndclass.hbrBackground  = gdi32.GetStockObject(WHITE_BRUSH)
        wndclass.lpszMenuName   = None
        wndclass.lpszClassName  = 'MainWin'

        user32.RegisterClassW(byref(wndclass))

        hwnd = user32.CreateWindowExW(0, 
                            wndclass.lpszClassName, 
                            'Python Window', 
                            WS_OVERLAPPEDWINDOW, 
                            CW_USEDEFAULT, 
                            CW_USEDEFAULT, 
                            CW_USEDEFAULT, 
                            CW_USEDEFAULT, 
                            None, 
                            None, 
                            wndclass.hInstance, 
                            None)


        msg = w.MSG()
        while user32.GetMessageW(byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(byref(msg))
            user32.DispatchMessageW(byref(msg))

        return msg.wParam

    def is_elevated(self) -> bool:
        if platform.system() == "Windows":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return False
        else:
            return os.geteuid() == 0
    
    def protect_process(self) -> int:
        if not self.is_elevated():
            return 0
        is_critical = ctypes.c_bool(True)
        result = RtlSetProcessIsCritical(True, ctypes.byref(is_critical), False)
        return 1 if result == 0 else 0

    def un_protect_process(self) -> int:
        if not self.is_elevated():
            return 0
        is_critical = ctypes.c_bool(False)
        result = RtlSetProcessIsCritical(False, ctypes.byref(is_critical), False)
        return 1 if result == 0 else 0
