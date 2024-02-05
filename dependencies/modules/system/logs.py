import os
import shutil
import processManagement
from ..constants import SYSTEMROOT

class Logs:
    @staticmethod
    def clear_logs():
        if processManagement.isElevated() != 1:
            return 0
        try:
            shutil.rmtree(os.path.join(SYSTEMROOT, "Logs"), ignore_errors = True)
            return 1
        except:
            return 0