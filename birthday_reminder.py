import pandas as pd
from datetime import date
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart

URL = 'https://docs.google.com/spreadsheets/d/140jENzG4GACjso1W9v4Lpl6onnRXZXQ6/export?format=xlsx'

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

recipient = os.getenv('recipient')
subject = 'Birthday Reminder!'

for index, row in df.iterrows():
    birthdate = row['BIRTHDATE(REGULARIZED)']
    name = row['YOUR FULL NAME ']
    
    if birthdate.month == t.month and birthdate.day == t.day:
        body = f"Today is {name}'s birthday!"
        
        send_birthday_email (recipient, subject, body)
