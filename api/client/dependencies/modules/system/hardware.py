from datetime import datetime
import psutil
from ..utils import byte_to_gb
from ..commands import Command, CommandArgs, ICommandModule, CommandResult
from pydantic import Field, ValidationError
from typing import Callable, Dict


class GetDiskUsageInfoArgs(CommandArgs):
    drive: str = Field(..., description="Drive letter or mount point to get disk usage info")

command_arg_map = {
    Command.GET_DISK_USAGE_INFO: GetDiskUsageInfoArgs,
    Command.GET_CPU_USAGE: None,
    Command.GET_RAM_USAGE_INFO: None,
    Command.GET_DISK_INFO: None,
    Command.GET_COMPLETE_SYS_INFO: None
}


class HardwareInfo(ICommandModule):
    @staticmethod
    def get_cpu_usage():
        usage = psutil.cpu_percent(interval=1)
        return CommandResult(success=True, result=f"CPU Usage: {usage}%")

    @staticmethod
    def get_disk_usage_info(args: GetDiskUsageInfoArgs) -> CommandResult:
        try:
            usage = psutil.disk_usage(args.drive)
            totalDisk = byte_to_gb(usage.total)
            usedDisk = byte_to_gb(usage.used)
            return CommandResult(success=True, result={"Total GB": totalDisk, "Used GB": usedDisk, "drive" : args.drive})
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    @staticmethod
    def get_ram_usage_info():
        try:
            mem = psutil.virtual_memory()
            totalRam = byte_to_gb(mem.total)
            usedRam = byte_to_gb(mem.used)
            return CommandResult(success=True, result={"Total GB": totalRam, "Used GB": usedRam})
        except Exception as e:
            return CommandResult(success=False, result=str(e))

    @staticmethod
    def get_disk_info():
        info = []
        for disk in psutil.disk_partitions():
            usage = psutil.disk_usage(disk.mountpoint)
            disk_info = {
                "Device": disk.device,
                "Mountpoint": disk.mountpoint,
                "Fstype": disk.fstype,
                "TotalSizeGB": byte_to_gb(usage.total),
                "UsedGB": byte_to_gb(usage.used),
                "FreeGB": byte_to_gb(usage.free),
                "PercentageUsed": usage.percent,
            }
            info.append(disk_info)
        return CommandResult(success=True, result=info)

    @staticmethod
    def get_system_info() -> CommandResult:
        try:
            info = {
                "CPU Usage": HardwareInfo.get_cpu_usage().result,
                "RAM Usage": HardwareInfo.get_ram_usage_info().result,
                "Disk Usage": [HardwareInfo.get_disk_usage_info(GetDiskUsageInfoArgs(drive=disk.mountpoint)).result for disk in psutil.disk_partitions()],
                "Boot Time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
                "Network Interfaces": {intf: [{"address": addr.address, "netmask": addr.netmask, "broadcast": addr.broadcast} for addr in addrs] for intf, addrs in psutil.net_if_addrs().items()},
                "Battery": HardwareInfo.get_battery_info(),
            }
            return CommandResult(success=True, result=info)
        except Exception as e:
            return CommandResult(success=False, result=str(e))
        
    @staticmethod
    def get_battery_info():
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "percent": battery.percent,
                    "seconds_left": battery.secsleft,
                    "plugged_in": battery.power_plugged
                }
            else:
                return "Battery information not available"
        except AttributeError:
            return "Battery sensors not supported on this system"

    def run(self, command: Command, args: CommandArgs = None) -> CommandResult:
        print(f"Command: {command} Args: {args}")
        command_func_map_with_args: Dict[Command, Callable[[CommandArgs], CommandResult]] = {
            Command.GET_DISK_USAGE_INFO: self.get_disk_usage_info,
        }
        
        command_func_map_no_args: Dict[Command, Callable[[], CommandResult]] = {
            Command.GET_CPU_USAGE: self.get_cpu_usage,
            Command.GET_RAM_USAGE_INFO: self.get_ram_usage_info,
            Command.GET_DISK_INFO: self.get_disk_info,
            Command.GET_COMPLETE_SYS_INFO: self.get_system_info
        }

        if command not in command_func_map_no_args and command not in command_func_map_with_args:
            return CommandResult(success=False, result="Error: Command not found in module.")

        try:
            if command in command_func_map_no_args:
                return command_func_map_no_args[command]()
            elif command in command_func_map_with_args:
                if args is None:
                    return CommandResult(success=False, result="No Args passed")
                validated_args = command_arg_map[command](**args.model_dump())
                return command_func_map_with_args[command](args=validated_args)
        except ValidationError as e:
            return CommandResult(success=False, result=f"Validation error: {e}")
        except Exception as e:
            return CommandResult(success=False, result=f"Error: {e}")

