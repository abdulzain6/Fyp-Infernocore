import subprocess, time, pyautogui, multiprocessing
from ..input_output import BlockInput
from ..input_output.window import minimize_all_windows

class TypeMessage:
    def _type(self, message, delayChar = 0):
        subprocess.Popen(["C:\\Windows\\notepad.exe"])
        time.sleep(2)
        for char in message:    
            pyautogui.press(char)
            time.sleep(delayChar)


    def type_message_notepad(self, message:str, blocktime, delayChar):
        try:
            blocktime = int(blocktime)
            delayChar = int(delayChar)
            minimize_all_windows()
            th = multiprocessing.Process(target = self._type, args = (message, delayChar))
            th.start()
            b = BlockInput()
            b.block_smart_seconds(blocktime)
        except Exception as e:
            print(e)





type_message_obj = TypeMessage()