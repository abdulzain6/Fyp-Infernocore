import psutil, signal, os

class Process:
    @staticmethod
    def get_processes():
        processes = []
        for proc in psutil.process_iter():
            try:
                processName = proc.name()
                processID = proc.pid
                processUsername = proc.username()
                processExe = proc.exe()
                processes.append((processName, processID, processUsername, processExe))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return processes

    @staticmethod
    def kill_process(pid):
        os.kill(pid, signal.SIGILL)





