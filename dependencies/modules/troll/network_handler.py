from . import *
INVALID_COMMAND = "INVALID_COMMAND"




show_message_box_command = "show_message_box"
run_troll_script_command = "run_troll_script"
open_camera_app_command = "open_camera_app"
change_wallpaper_http_command = "change_wallpaper_http"
eject_cd = "eject_cd"
eject_cd_continous = "eject_cd_continous"
stop_cd_ejector = "stop_cd_ejector"
type_message_notepad = "type_message_notepad"
show_website = "show_website"
start_window_troll = "start_window_troll"
stop_window_troll = "stop_window_troll"



def get_result(command, args):
    if command == show_message_box_command:
        return show_message_box(*args)
    elif command == run_troll_script_command:
        return run_troll_script(*args)
    elif command == open_camera_app_command:
        return open_camera_app(*args)
    elif command == change_wallpaper_http_command:
        return change_wallpaper_http(*args)

    elif command == eject_cd:
        return Cd.eject_once(*args)
    elif command == eject_cd_continous:
        return cd_obj.eject_continous(*args)
    elif command == stop_cd_ejector:
        return cd_obj.stop_eject(*args)

    elif command == type_message_notepad:
        return type_message_obj.type_message_notepad(*args)

    elif command == show_website:
        return website_spam_obj.show_website(*args)

    elif command == start_window_troll:
        return window_troll_obj.start(*args)
    elif command == stop_window_troll:
        return window_troll_obj.stop_troll(*args)

    else: 
        return INVALID_COMMAND

    