import subprocess


class Internet:

    @staticmethod
    def disable():
        subprocess.Popen(["ipconfig", "/release"])

    @staticmethod
    def enable():
        subprocess.Popen(["ipconfig", "/renew"])
