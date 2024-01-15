import os
import json
from functions import email,log

def alert(message):
    email(f'{os.popen("hostname").read()} closed ports have been found:',
f"""
{message}
""")

# Dump IP information to from the OS and convert to JSON
output = os.popen("ip -4 -p -h -c -j address").read()
output = json.loads(output)

# Placeholder dictionary to add IP's and port statuses 
ipList= {}

try:

    def portTest():
        
        # Check the 'local' adaptor for all attached IP's
        for x in output:
            if x['ifname'] != 'lo':
                for z in range(len(x['addr_info'])):
                    if len(x['addr_info'][z]['local']) < 16:
                        ipList[x['addr_info'][z]['local']] = 'None'


        # Check all listed IP's ports and add their status to the dictionary
        for item in ipList:
            ipList[item] = os.popen(f"curl --interface {item} https://mnowatch.org/9999/").read()


        # Craft an email message which contains the IP of any closed ports
        email_body = ''
        for item in ipList:
            if ipList[item] == 'CLOSED':
                log('ports',f'port closed on {item}')
                email_body = email_body+ f"{item}\n"


        # Send an email alert only if the message body isn't empty
        if len(email_body) > 0:
            alert(email_body)

except Exception as E:
    log('ports',E)
except KeyboardInterrupt:
    print("Bye!")