# Available Scripts: hacked, eainstaller, speakMessage, virusBox, writeMessage, showMessage, toogleLocks
#Note : speakMessage, writeMessage needs to be formatted with some text.

toogleLocks = """
On Error Resume Next
set wshShell =wscript.CreateObject(\"WScript.shell\")
do
wscript.sleep 5
wshshell.sendkeys \"{CAPSLOCK}\"
wscript.sleep 5
wshshell.sendkeys \"{NUMLOCK}\"
wscript.sleep 5
wshshell.sendkeys \"{SCROLLLOCK}\"
loop
On Error GoTo 0
"""

hacked = """
x=msgbox(\"Welcome. This application will install EA CRICKET07 in your computer. Click OK to Continue\", 1+64, \"EA CRICKET 07\")
x=msgbox(\"The application was unable to search for a Drive Folder. Click RETRY.\",5+16, \"EA CRICKET 07\")
x=msgbox(\"Willing to continue?   \",0+32, \"CORRUPTION MODE ON\")
x=msgbox(\"Your Anti-Virus Software is Disabled by the Secuirty Breacher   \",0+48, \"HACKING PROECESS ON\")
x=msgbox(\"Your Files are being corrupted... \",0+48, \"HACKING PROECESS ON\")
x=msgbox(\"Checking the security key and exploiting the weakness in your computer...  \",0+64, \"HACKING PROECESS ON\")
x=msgbox(\"ALL DEFENSES SUCCESSFULLY BREACHED... \",0+48, \"HACKING PROECESS ON\")
x=msgbox(\"Importing all your files to a hidden folder... \",0+16, \"HACKING PROECESS ON\")
x=msgbox(\"Your files have been succesfully collected by the security breacher \",0+48, \"HACKING PROECESS ON\")
Do
x=msgbox(\"YOUR SYSTEM IS NOW HACKED. ALL YOUR MOVEMENTS WILL BE WATCHED AND ANALYSED \",0+64, \"HACKING PROECESS DONE\")
Loop
"""

eaInstaller = """
x=msgbox(\"Welcome. This application will install EA CRICKET07 in your computer. Click OK to Continue\", 1+64, \"EA CRICKET 07\")
x=msgbox(\"The application was unable to search for a Drive Folder. Click RETRY.\",5+16, \"EA CRICKET 07\")
x=msgbox(\"Willing to continue?   \",0+32, \"CORRUPTION MODE ON\")
x=msgbox(\"Your Anti-Virus Software is Disabled by the Secuirty Breacher   \",0+48, \"HACKING PROECESS ON\")
x=msgbox(\"Your Files are being corrupted... \",0+48, \"HACKING PROECESS ON\")
x=msgbox(\"Checking the security key and exploiting the weakness in your computer...  \",0+64, \"HACKING PROECESS ON\")
x=msgbox(\"ALL DEFENSES SUCCESSFULLY BREACHED... \",0+48, \"HACKING PROECESS ON\")
x=msgbox(\"Importing all your files to a hidden folder... \",0+16, \"HACKING PROECESS ON\")
x=msgbox(\"Your files have been succesfully collected by the security breacher \",0+48, \"HACKING PROECESS ON\")
x=msgbox(\"YOUR SYSTEM IS NOW HACKED. ALL YOUR MOVEMENTS WILL BE WATCHED AND ANALYSED \",0+64, \"HACKING PROECESS DONE\")
x=msgbox(\"BUY A NEW COMPUTER (OR) BE OBSERVED BY AN UNKNOWN HACKER \",0+48, \"WARNING\")
"""

speakMessage = """        
On Error Resume Next
Dim Message, Speak
Message=\"{}\"
Set Speak=CreateObject(\"sapi.spvoice\")
Speak.Speak Message
On Error GoTo 0
"""

virusBox = """
Do
x=msgbox(\"You Have Received a Dangerous Virus, Please Call Norton Security Hotline at, 1-800-473-7503 Please Call As Soon As You Can So Your Banking Information and Personal Information Do Not Become Leaked and, and Photos and Videos Will Not Be Corrupted. 										        -Thank You for Choosing Nortonï¿½\", 16, \"Norton Security Warning (Powered by, Nortonï¿½)\")
Loop
"""

writeMessage = """
set wshShell =wscript.CreateObject(\"WScript.shell\")
WshShell.SendKeys \"{}\"
"""

toogleLocks = """
On Error Resume Next
set wshShell =wscript.CreateObject(\"WScript.shell\")
do
wscript.sleep 5
wshshell.sendkeys \"{CAPSLOCK}\"
wscript.sleep 5
wshshell.sendkeys \"{NUMLOCK}\"
wscript.sleep 5
wshshell.sendkeys \"{SCROLLLOCK}\"
loop
On Error GoTo
"""

showMessage = """
x=msgbox(\"{}\",0+64, \"{}\")
"""

