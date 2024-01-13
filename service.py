import os

    
cwd = os.getcwd()
fullpath = f"{cwd}/nodemonitor.py"

if not os.path.exists("/etc/systemd/system"):
    os.mkdir("/etc/systemd/system")
if os.path.exists("/etc/systemd/system/nodemonitor.service"):
    os.remove("/etc/systemd/system/nodemonitor.service")
with open("/etc/systemd/system/nodemonitor.service", "w") as w:
    w.write(f"""\
[Unit]
Description=Masternode & Server alerting script
After=syslog.target network-online.target


[Service]
Type=simple

OOMScoreAdjust=-1000

ExecStart=/usr/bin/python3 {fullpath}
TimeoutStartSec=10m

Restart=on-failure
RestartSec=15

StartLimitInterval=15
StartLimitBurst=3

[Install]
WantedBy=multi-user.target
""")
    
os.system("systemctl enable --now nodemonitor.service")

print("""
Service file has been installed - you can now quit the process and it should automatically restart
You can start, stop and check the status of the service with

systemctl start nodemonitor
systemctl stop nodemonitor
systemctl status nodemonitor

""")