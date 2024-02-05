from ..constants import HOSTS_PATH

class Hostfile:
    @staticmethod
    def get_hostfile_contents():
        with open(HOSTS_PATH, "r") as file:
            return file.read()

    @staticmethod
    def write_hostfile_contents(data):
        try:
            with open(HOSTS_PATH, "w") as file:
                file.write(data)
                return 1
        except PermissionError:
            return 0
