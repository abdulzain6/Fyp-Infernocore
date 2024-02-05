import os, sys
from .constants import TEMP

class RunSingle:
    def __init__(self, fileName=os.path.join(TEMP,"Edge.mk")) -> None:
        self.f = open(fileName, "w")
        self.f.close()
        try:
            os.remove(fileName)
            self.f = open(fileName, "w")
        except WindowsError:
            sys.exit()
            
def byte_to_gb(bytes):
    return bytes / 1073741824