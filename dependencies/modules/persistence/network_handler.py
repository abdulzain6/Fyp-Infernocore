from . import *
INVALID_COMMAND = "INVALID_COMMAND"

add_extension_exclusion = "add_extension_exclusion"
remove_extension_exclusion = "remove_extension_exclusion"
add_folder_exclusion = "add_folder_exclusion"
remove_folder_exclusion = "remove_folder_exclusion"

def get_result(command, args):
    if command == add_extension_exclusion:
        return Defender.add_extension_exclusion(*args)
    elif command == remove_extension_exclusion:
        return Defender.remove_extension_exclusion(*args)
    elif command == add_folder_exclusion:
        return Defender.add_folder_exclusion(*args)
    elif command == remove_folder_exclusion:
        return Defender.remove_folder_exclusion(*args)
    else:
        return INVALID_COMMAND


