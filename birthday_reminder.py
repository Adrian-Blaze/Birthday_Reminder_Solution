import pandas as pd
from datetime import date
import smtplib
from email.mime.text import MIMEText
import os
import json
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from zoneinfo import ZoneInfo
from datetime import datetime

URL = os.getenv('URL').strip()


#t = date.today()
t = date(2024, 6, 1)
df = pd.read_excel(URL)
birthdates = df[['BIRTHDATE(REGULARIZED)', 'YOUR FULL NAME ']]
load_dotenv()
EMAIL_ADDRESS = os.getenv('Email_Address')
EMAIL_PASSWORD = os.getenv('Email_Password')
SMTP_SERVER = 'smtp.gmail.com'
PORT = 587

def send_birthday_email(recipient_email, subject, body):
    for recipient in recipient_email:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            with smtplib.SMTP(SMTP_SERVER, PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
            print(f'Email sent sucessfully')
        except Exception as e:
            print(f'Failed to send email: {e}')

def log_birthday(name):
    """
    Logs a birthday event to log.txt with timestamp.
    """
    timestamp = datetime.now(ZoneInfo("Africa/Lagos")).strftime('%Y-%m-%d %H:%M')

    with open("log.txt", "a") as f:
        f.write(f"{timestamp} - Birthday: {name}\n")

recipient = json.loads(os.getenv("recipient").strip())
subject = 'Birthday Reminder!'

for index, row in df.iterrows():
    birthdate = row['BIRTHDATE(REGULARIZED)']
    name = row['YOUR FULL NAME ']
    
    if birthdate.month == t.month and birthdate.day == t.day:
        body = f"Today is {name}'s birthday!"
        
        send_birthday_email (recipient, subject, body)
        log_birthday(name)
