import os
import importlib.util


# Check if 'psutil' is installed - if not, install and import
if importlib.util.find_spec('psutil') is None:
    os.system('pip3 install psutil')
    import psutil


# Finish importing required modules
from objects import Sys
from time import sleep
from functions import email,log
from ports import portTest


# Define an email alert message to be 
def alert(alarm, value):
    email(f'{os.popen("hostname").read()} {alarm} alarm: {value}',
f"""
CPU 10min Average: {monitor.cpu10min}%
Disk Used: {monitor.disk}%
Swap Memory: {monitor.swap}%
Virtual Memory: {monitor.vm}%
Combined Memory Used: {round(monitor.mem,2)}%
""")


try:
    # Specify how many emails you would like to receive after a restart
    # Emails are sent every 10 minutes until the counter is reached
    afterBoot = 1
    portTestFrequency = 600


    portTestTimer = 0

    # Start the monitoring script
    while True:

        # Find all IP's and carry out a port test on each
        if portTestTimer > portTestFrequency:
            portTest()
            portTestTimer = 0
        else:
            portTestTimer += 10

        # Call the monitor class which polls resource sensors
        monitor = Sys(afterBoot)

        # Monitor CPU usage which is averaged over 10 minutes
        # Allow 15 minutes before first alert is sent to allow system to stabilize
        if monitor.cpu10min > 95 and monitor.cpu10minAlarm == False and monitor.uptime > 900:
            monitor.cpuAlarmToggle()
            log('nodemonitor','CPU usage high')
            alert('cpu 10 min average high', monitor.cpu10min)
        elif monitor.cpu10min < 80 and monitor.cpu10minAlarm:
            log('nodemonitor','CPU usage has returned to normal')
            monitor.cpuAlarmToggle()
            alert('cpu restored', monitor.cpu10min)

        # Monitor free memory - (VM % + Swap %) / 2
        if monitor.mem > 80 and monitor.memAlarm == False:
            log('nodemonitor','Combined memory is high')
            monitor.memAlarmToggle()
            alert('combined memory high', monitor.mem)
        elif monitor.mem < 70 and monitor.memAlarm:
            log('nodemonitor','Combined memory has returned to normal')
            monitor.memAlarmToggle()
            alert('memory restored', monitor.mem)

        # Monitor free disk space
        if monitor.disk > 95 and monitor.diskAlarm == False:
            log('nodemonitor','Disk usage is high')
            monitor.diskAlarmToggle()
            alert('disk usage high', monitor.disk)
        elif monitor.disk < 85 and monitor.diskAlarm:
            log('nodemonitor','Disk usage returned to normal')
            monitor.diskAlarmToggle()
            alert('disk usage restored', monitor.disk)
        
        # Before combined free memory runs out, send an email alert and reboot immediately
        if monitor.mem > 96:
            log('nodemonitor','Combined memory critical, rebooting')
            alert('oom, rebooting', monitor.mem)
            os.system("reboot")

        sleep(10)

except Exception as E:
    log('nodemonitor',E)
except KeyboardInterrupt:
    print("Bye!")