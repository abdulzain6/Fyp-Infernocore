from ctypes import wintypes
import ctypes


def reverse_mouse_button(restore = False):
    restore = int(restore)
    func = ctypes.windll.user32.SwapMouseButton
    func.argtypes = [wintypes.BOOL]
    func.restype = wintypes.BOOL
    return func(True) if not restore else func(False)