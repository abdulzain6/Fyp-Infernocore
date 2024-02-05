import contextlib
import json
import queue
import socket
import threading
import time
from enum import Enum
from typing import Dict, List, Set, Tuple


class InitCommands(Enum):
    GET_CLIENTS_INIT_COMMAND: str = "CLIENTS"
    START_PINGER_INIT_COMMAND: str = "PINGER"

class ErrorMessages(Enum):
    CLIENT_DOESNT_EXIST_ERROR: str = "ERROR_CLIENT_DOESNT_EXIST"


class Server:
    def __init__(self, LEN_SIZE: int = 100000, CLIENT_STRING: str = "client", USER_STRING: str = "user", PORT: int = 9999, ADDRESS: str = "") -> None:
        self.main_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port_to_listen: int = PORT
        self.address: str = ADDRESS
        
        self.clients: List[socket.socket] = []
        self.users: Set[Tuple[socket.socket, socket._RetAddress]] = set()
        self.started_recieving_from: List[socket.socket] = []
        self.user_commands: queue.Queue = queue.Queue()

        self.LEN_SIZE: int = LEN_SIZE
        self.CLIENT_STRING: str = CLIENT_STRING
        self.USER_STRING: str = USER_STRING

    def start_server(self) -> None:
        """Function to start the server
        """
        self.main_socket.bind((self.address, self.port_to_listen))
        self.main_socket.listen()
        while True:
            con, addr = self.main_socket.accept()
            con.setblocking(1)
            t = threading.Thread(
                target=self.handle_user_and_client, args=(con, addr))
            t.start()

    def verify_creds(self, user_name: str, password: str) -> bool:
        """Function to verify the credentials of the user.

        Args:
            user_name (str): The username of the user
            password (str): The password of the user.

        Returns:
            bool: True indicates the authentication was successful, False, Vice versa.
        """
        return True


    def recieve(self, con: socket.socket, decode: bool = True) -> str | bytes:
        """Dynamic recieve method to first recieve the size then recieve the message

        Args:
            con (socket object returned by socket.accept())

        Returns:
            message: The message recieved from the connection.
        """
        while True:
            try:
                message = con.recv(self.LEN_SIZE).decode('utf-8')
                message_size = int(message)
                return (
                    con.recv(message_size).decode("utf-8")
                    if decode
                    else con.recv(message_size)
                )

            except socket.error:
                break
                

    def recieve_no_error_check(self, con: socket.socket, decode: bool = True) -> str | bytes:
        message = con.recv(self.LEN_SIZE).decode('utf-8')
        message_size = int(message)
        return (
            con.recv(message_size).decode("utf-8")
            if decode
            else con.recv(message_size)
        )

    def send_message(self, message: str, con: socket.socket, encode: bool = True) -> None:
        length_of_message = str(len(message))
        spaces_to_add = self.LEN_SIZE - len(length_of_message)
        message = length_of_message + " "*spaces_to_add + message
        if encode:
            con.send(message.encode())
        else:
            con.send(message)

    def get_clients(self) -> Dict[int, socket.socket]:
        return {i: client[1] for i, client in enumerate(self.clients, start=1)}


    def recieve_response(self, con: socket.socket) -> None:
        print("[+] Reciever started")
        while True:
            try:
                print("[+] Message to client sent, now recieving response")
                message_from_client = self.recieve(con)
                print(message_from_client)
                ip, port = self.get_user_ip_port(message_from_client)
                user_con = self.get_user_by_ip_port(ip ,port)
                print("[+] Message recieved from client ", message_from_client)
                print("[+] Sending message to user ", message_from_client)
                self.send_message(message_from_client, user_con)
                print("[+] Message to user sent, now recieving")
            except socket.error:
                break



    def handle_user(self, con: socket.socket, addr: socket._RetAddress) -> None:
        while True:
            try:
                message = self.recieve(con)
                if self.check_for_server_commands_for_user(message, con, addr) == 0:
                    self.users.add((con, addr))
                    message = json.loads(message)
                    message["user"] = addr
                    message = json.dumps(message)
                    print(message)
                    target_ip, target_port = self.get_client_ip_port(message)    
                    if client_con := self.get_client_by_ip_port(target_ip, target_port):
                        self.send_message(message, client_con)
                    else:
                        self.send_message(json.dumps({"result" : ErrorMessages.CLIENT_DOESNT_EXIST_ERROR}), con)
            except Exception:
                break

    def handle_client(self, con: socket.socket, addr: socket._RetAddress) -> None:
        message = self.recieve(con)
        if self.check_for_server_commands_for_client(message, con) == 0:
            self.clients.append((con, addr))
            print("New client joined", addr)
            self.recieve_response(con)


    def check_for_server_commands_for_user(self, message: str, con: socket.socket, addr: socket._RetAddress) -> int:
        try:
            message = json.loads(message)
            server_command = message["server_command"]
            if server_command == InitCommands.GET_CLIENTS_INIT_COMMAND:
                self.send_available_clients((con, addr))
            elif server_command == InitCommands.START_PINGER_INIT_COMMAND:
                self.recieve_pings(con)
            else:
                return 0
        except Exception:
            return 0
        
    def check_for_server_commands_for_client(self, message: str, con: socket.socket) -> int:
        try:
            message = json.loads(message)
            server_command = message["server_command"]
            if server_command == InitCommands.START_PINGER_INIT_COMMAND:
                self.recieve_pings(con)
            else: 
                return 0
        except Exception:
            return 0

    def get_user_ip_port(self, message: str) -> Tuple[str, str]:
        message = json.loads(message)
        origin_ip = message["user"][0]
        origin_port = message["user"][1]
        return origin_ip, origin_port

    def get_client_ip_port(self, message: str) -> Tuple[str, str]:
        message = json.loads(message)
        target_ip = message["ip"]
        target_port = message["port"]
        return target_ip, target_port

    def get_client_by_ip_port(self, ip: str, port: str) -> socket.socket:
        return next(
            (
                c[0]
                for c in self.clients
                if c[1][0] == ip and int(c[1][1]) == int(port)
            ),
            None,
        )

    def get_user_by_ip_port(self, ip: str, port: str) -> socket.socket:
        return next(
            (
                c[0]
                for c in self.users
                if c[1][0] == ip and int(c[1][1]) == int(port)
            ),
            None,
        )


    def recieve_pings(self, con: socket.socket) -> None:
        ip = ""
        port = ""
        while True:
            try:
                data = self.recieve_no_error_check(con)
                data = json.loads(data)
                ip = data["ip"]
                port = data["port"]
            except socket.error:
                is_client = False
                for client in self.clients:
                    if client[1] == (ip, int(port)):
                        self.clients.remove(client)
                        print(f"{client[1]} left")
                        is_client = True
                        break

                if is_client:
                    break

                for user in self.users:
                    if user[1] == (ip, int(port)):
                        self.users.remove(user)
                        print(f"{user[1]} left")
                        break
                break
            except Exception as e:
                print("Pinger ", e)


    def send_available_clients(self, user_info: Tuple[socket.socket, socket._RetAddress]) -> None:
        while True:
            try:
                self.send_message(json.dumps(self.get_clients()), user_info[0])
                time.sleep(3)
            except socket.error:
                break

    def handle_user_and_client(self, con: socket.socket, addr: socket._RetAddress) -> None:
        with contextlib.suppress(Exception):
            init_message = self.recieve(con)
            init_message = json.loads(init_message)
            if init_message["role"] == self.USER_STRING and self.verify_creds(init_message["username"], init_message["password"]) == True:
                self.handle_user(con, addr)

            elif init_message["role"] == self.CLIENT_STRING:
                self.handle_client(con, addr)


server = Server()
server.start_server()
