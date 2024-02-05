import psutil
from ..utils import byte_to_gb
from ..scripting_interface import execute_powershell_script

class HardwareInfo:
    @staticmethod
    def get_cpu_usage():
        return psutil.cpu_percent()

    @staticmethod
    def get_disk_usage_info(drive):
        try:
            totalDisk = byte_to_gb(psutil.disk_usage(drive)[0])
            usedDisk = byte_to_gb(psutil.disk_usage(drive)[1])
            return (totalDisk, usedDisk)
        except:
            return (None, None)

    @staticmethod
    def get_ram_usage_info():
        try:
            totalRam = byte_to_gb(psutil.virtual_memory()[0])
            usedRam = byte_to_gb(psutil.virtual_memory()[3])
            return (totalRam, usedRam)
        except:
            return (None, None)

    @staticmethod
    def get_disk_info():
        info = []
        data = execute_powershell_script("Get-Disk | Format-List", getOutput=True).split("\n\r\n")
        for disk in data:
            disk_dict = {}
            disk_split = disk.split("\n")
            for d in disk_split:
                if "Model" in d:
                    disk_dict["Model"] = d.replace("Model              : ", "").strip()
                elif "Size" in d:
                    disk_dict["Size"] = d.replace("Size               : ", "").strip()
                elif "UniqueId" in d:
                    disk_dict["UniqueId"] = d.replace("UniqueId           : ", "").strip()
                elif "Number" in d:
                    disk_dict["Number"] = d.replace("Number             : ", "").strip()
                elif "Path" in d:
                    disk_dict["Path"] = d.replace("Path               : ", "").strip()
                elif "Manufacturer" in d:
                    disk_dict["Manufacturer"] = d.replace("Manufacturer       : ", "").strip()
                elif "AllocatedSize" in d:
                    disk_dict["AllocatedSize"] = d.replace("AllocatedSize      : ", "").strip()
                elif "LogicalSectorSize" in d:
                    disk_dict["LogicalSectorSize"] = d.replace("LogicalSectorSize  : ", "").strip()
                elif "PhysicalSectorSize" in d:
                    disk_dict["PhysicalSectorSize"] = d.replace("PhysicalSectorSize : ", "").strip()
                elif "NumberOfPartitions" in d:
                    disk_dict["NumberOfPartitions"] = d.replace("NumberOfPartitions : ", "").strip()
                elif "IsReadOnly" in d:
                    disk_dict["IsReadOnly"] = d.replace("IsReadOnly         : ", "").strip()     
                elif "PartitionStyle" in d:
                    disk_dict["PartitionStyle"] = d.replace("PartitionStyle     : ", "").strip()  
                elif "IsSystem" in d:
                    disk_dict["IsSystem"] = d.replace("IsSystem           : ", "").strip()  
                elif "IsBoot" in d:
                    disk_dict["IsBoot"] = d.replace("IsBoot             :", "").strip()                                             
            info.append(disk_dict)
            
        return info
