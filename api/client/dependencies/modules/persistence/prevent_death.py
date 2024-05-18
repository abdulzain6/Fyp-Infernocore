import subprocess
import multiprocessing
import threading
import time
import sys
import psutil
import os
import platform



class ProcessManager:
    def __init__(self, number_of_children):
        self.number_of_children = number_of_children
        self.main_pid = os.getpid()

    def child_task(self, main_pid, child_id):
        """ Function to handle child tasks. """
        while True:
            if not psutil.pid_exists(main_pid):
                self.handle_process_death()
            time.sleep(2)

    def handle_process_death(self):
        """ Cross-platform function to handle process death by restarting the computer. """
        print("Handling process death. Attempting to restart the computer...")
        try:
            if platform.system() == "Windows":
                subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
            elif platform.system() == "Linux" or platform.system() == "Darwin":
                subprocess.run(["shutdown", "-r", "now"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to restart the computer: {e}")
            
    def monitor_children(self, child_processes):
        """ Thread function to monitor the child processes """
        while any(p.is_alive() for p in child_processes):
            time.sleep(1)  # Check every second
        # If any child process is not alive, handle process death
        self.handle_process_death()

    def run(self):
        child_processes = []
        for i in range(self.number_of_children):
            process = multiprocessing.Process(target=self.child_task, args=(self.main_pid, i))
            process.start()
            child_processes.append(process)
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_children, args=(child_processes,))
        monitor_thread.start()
        return child_processes, monitor_thread

    def join(self, child_processes, monitor_thread):
        for p in child_processes:
            p.join()
        monitor_thread.join()