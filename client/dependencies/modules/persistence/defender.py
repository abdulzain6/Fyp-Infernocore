import processManagement
from .. import scripting_interface
from ...scripts.powershell_scripts.system import addExtensionExclusionScript, removeExtensionExclusionScript, addFolderExclusionScript, removeFolderExclusionScript, disableSamplingScript

class Defender:
    @staticmethod
    def add_extension_exclusion(extension:str):
        if "." in extension:
            extension = extension.replace(".", "")
        if processManagement.isElevated() != 1:
            return 0
        scripting_interface.execute_powershell_script(addExtensionExclusionScript.format(extension))
        return 1

    @staticmethod
    def remove_extension_exclusion(extension:str):
        if "." in extension:
            extension = extension.replace(".", "")
        if processManagement.isElevated() != 1:
            return 0
        scripting_interface.execute_powershell_script(removeExtensionExclusionScript.format(extension))
        return 1
    
    @staticmethod
    def add_folder_exclusion(path:str):
        if processManagement.isElevated() != 1:
            return 0
        scripting_interface.execute_powershell_script(addFolderExclusionScript.format(path))

    @staticmethod
    def remove_folder_exclusion(path:str):
        if processManagement.isElevated() != 1:
            return 0
        scripting_interface.execute_powershell_script(removeFolderExclusionScript.format(path))

    @staticmethod
    def stop_sampling():
        if processManagement.isElevated() != 1:
            return 0
        scripting_interface.execute_powershell_script(disableSamplingScript)