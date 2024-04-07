ping_scan = """
@ECHO Off
set startTime=%time%
ECHO Starting the IP Scan
FOR /L %%i IN ({} ,1, {}) DO @(
ECHO Pinging IP Range: 192.168.%%i._
FOR /L %%z IN ({} ,1, {}) DO @(
echo Pinging IP: 192.168.%%i.%%z
ping -n 1 -w 500 192.168.%%i.%%z | FIND /i "Reply"
)
)
echo fooling_the_OS
"""