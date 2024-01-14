import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from credentials import *
from datetime import datetime

def email(subject,body):
    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        body = MIMEText(body)

        obj = MIMEBase('application','octet-stream')
        obj.add_header('Content-Disposition',"attachment")
        message.attach(body)
        my_message = message.as_string()
        email_session = smtplib.SMTP(sender_mailserver,sender_port)
        email_session.starttls()
        email_session.login(sender_email,sender_password)
        email_session.sendmail(sender_email,recipient_email,my_message)
        email_session.quit()
    except Exception as E:
        print(f'Error sending email - {E}')



def log(script,message):
    
    # datetime object containing current date and time
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    with open(debug,"a") as l:
        l.write(f"{now} - {script} - {message}")


        


 

