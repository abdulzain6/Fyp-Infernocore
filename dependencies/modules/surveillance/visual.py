import contextlib
import ctypes
from PIL import ImageGrab
import base64

class Visuals:
    @staticmethod
    def screenshot():
        with contextlib.suppress(Exception):
            ctypes.windll.user32.SetProcessDPIAware()
        image = ImageGrab.grab()
        h, w = image.size
        m = image.mode
        im =  base64.b64encode(image.tobytes()).decode('ascii')
        return {"size" : (h,w), "mode" : m, "image" : im}

    



