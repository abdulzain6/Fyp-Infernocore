#Available Scripts: showNotification

showNotification = """
Add-Type -AssemblyName System.Windows.Forms
$global:balmsg = New-Object System.Windows.Forms.NotifyIcon
$path = (Get-Process -id $pid).Path
$balmsg.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($path)
$balmsg.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Warning
$balmsg.BalloonTipText = '{}'
$balmsg.BalloonTipTitle = '{}'
$balmsg.Visible = $true
$balmsg.ShowBalloonTip({})
"""
playWindowsSoundContinously = """
param([Parameter()][int]$Interval = 4);
Get-ChildItem C:\Windows\Media\ -File -Filter *.wav | Select-Object -ExpandProperty Name | Foreach-Object { Start-Sleep -Seconds $Interval;
(New-Object Media.SoundPlayer "C:\WINDOWS\Media\$_").Play();
 }
"""