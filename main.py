import multiprocessing
import threading
from dependencies.modules.persistence.startup import Startup
import pickle




if __name__ == '__main__':
    Startup.add_to_registry("python.exe")