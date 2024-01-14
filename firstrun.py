import os

filename = 'credentials.py'

cwd = os.getcwd()
debug = cwd'/debug.log'
fullpath = f"{cwd}/{filename}"
response = input(f"""
                 
The following prompt will ask you for credentials and parameters 
required to send email alerts via SMTP as well as a recipient email 
address
                 
Please note that this information will be saved in plain text in the 
following file: {fullpath}

Would you like to continue? (y/n): """)

if response != 'y':
    exit()


recipient = input("Enter the receiving address for Email alerts: ")
sender = input("Enter the Email address used to log into the SMTP server: ")
password = input("Enter the Password used to log into the SMTP server: ")
mailserver = input("Enter the SMTP server address (eg smtp.serveraddress.com): ")
port = input("Enter the SMTP port number: ")


with open(fullpath, "w") as w:
        w.write(f"""
                
recipient_email = '{recipient}'
sender_email = '{sender}'
sender_password = '{password}'
sender_mailserver = '{mailserver}'
sender_port = '{port}'
debug = '{debug}

""")
        
print("Credentials have been saved - Starting the main script...")

import service
import nodemonitor