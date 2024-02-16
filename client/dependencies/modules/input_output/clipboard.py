from pyperclip import copy, paste
import time

class Clipboard():
    def __init__(self):
        self.isClipboardFillerOn = False

    @staticmethod
    def copy_text(text:str):
        copy(text)

    @staticmethod
    def get_text():
        return paste()

    def clipboard_filler(self, text:str, sleep):
        self.isClipboardFillerOn = True
        while self.isClipboardFillerOn:
            self.copy_text(text)
            time.sleep(sleep)

    def filler_off(self):
        self.isClipboardFillerOn = False


clipboard_obj = Clipboard()