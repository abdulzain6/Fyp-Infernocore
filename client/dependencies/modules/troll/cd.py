import ctypes, time

class Cd:
    def __init__(self) -> None:
        self.eject = False
    
    @staticmethod
    def eject_once():
        try:
            ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
            return 1
        except:
            return 0
    
    def eject_continous(self, delay):
        self.eject = True
        delay = int(delay)
        while self.eject:
            ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)
            time.sleep(delay)

    def stop_eject(self):
        self.eject = False
    

cd_obj = Cd()