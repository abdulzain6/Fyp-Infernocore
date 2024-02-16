from ..constants import *
from ..scripting_interface import *
from ...scripts.powershell_scripts.system import geoLocate
import csv, ctypes

class SysInfo:
    @staticmethod
    def get_system_info():
        data = subprocess.check_output([os.path.join(SYSTEM_32, "systeminfo"), "/FO", "CSV"]).decode('utf-8', errors = "ignore").split("\n")
        data = csv.reader(data)
        row1 = next(data)
        row2 = next(data)
        return dict(zip(row1[:-3], row2[:-3]))

    @staticmethod
    def get_uptime():
        lib = ctypes.windll.kernel32
        t = lib.GetTickCount64()
        t = int(str(t)[:-3])

        # extracting hours, minutes, seconds & days from t
        mins, sec = divmod(t, 60)
        hour, mins = divmod(mins, 60)
        days, hour = divmod(hour, 24)
        from collections import namedtuple
        Uptime = namedtuple("UpTime", ['days', 'hour', 'mins', 'secs'])
        return Uptime(days, hour, mins, sec)

    @staticmethod
    def get_username():
        return os.getlogin()

    @staticmethod
    def geo_locate():
        try:
            data = execute_powershell_script(geoLocate, True)
        except subprocess.CalledProcessError:
            return (0, 0)
        if "Denied" not in data:
            return tuple(data.split("\n")[2].split(" "))
        else:
            return (0, 0)

    