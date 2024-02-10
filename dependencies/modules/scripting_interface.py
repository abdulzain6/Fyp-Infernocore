from random import randrange
from io import StringIO
from contextlib import redirect_stdout
from .constants import *
import subprocess, os

def execute_powershell_script(script, getOutput = False, wait = False, createNewConsole = False):
    if getOutput:
        return (
            subprocess.check_output([POWERSHELL_PATH, script])
            .decode('utf-8', errors = 'ignore')
            .strip()
        )

    if createNewConsole:
        p = subprocess.Popen([POWERSHELL_PATH , script], creationflags = subprocess.CREATE_NEW_CONSOLE)
    else:
        p = subprocess.Popen([POWERSHELL_PATH , script])

    if wait:
        p.wait()


def execute_vb_script(script, wait = False):
    fname = f'{os.path.join(TEMP, str(randrange(1, 500000)))}.vbs'
    with open(fname, "w") as file:
        file.write(script)
    p = subprocess.Popen([WSCRIPT_PATH , fname], subprocess.CREATE_NEW_CONSOLE)
    if wait:
        p.wait()

def execute_batch_script(script, getOutput = False, wait = False, createNewConsole = True):
    fname = f'{os.path.join(TEMP, str(randrange(1, 500000)))}.bat'
    with open(fname, "w") as file:
        file.write(script)

    if getOutput:
        return subprocess.check_output([CMD_PATH, "/c", fname]).decode('utf-8', errors = 'ignore').strip()

    if createNewConsole:
        p = subprocess.Popen([CMD_PATH, "/c", "start", fname] , subprocess.CREATE_NEW_CONSOLE)
    else:
        p = subprocess.Popen([CMD_PATH, "/c", "start", fname])

    if wait:
        p.wait()

def execute_python_script(script):
    f = StringIO()
    with redirect_stdout(f):
        exec(script)
    return f.getvalue()


