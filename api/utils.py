import os

def get_script_path_and_append(subpaths: list[str]) -> str:
    # Get the current script file location
    current_file = os.path.abspath(__file__)

    # Get the directory of the current script
    base_dir = os.path.dirname(current_file)

    # Append multiple nested paths safely
    full_path = base_dir
    for subpath in subpaths:
        full_path = os.path.join(full_path, subpath)

    return full_path
