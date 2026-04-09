import pandas as pd
from datetime import date
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart

url = 'https://docs.google.com/spreadsheets/d/140jENzG4GACjso1W9v4Lpl6onnRXZXQ6/export?format=xlsx'

t = date.today()
df = pd.read_excel(url)
birthdates = df[['BIRTHDATE(REGULARIZED)', 'YOUR FULL NAME ']]
load_dotenv()
EMAIL_ADDRESS = os.getenv('Email_Address')
EMAIL_PASSWORD = os.getenv('Email_Password')
SMTP_SERVER = 'smtp.gmail.com'
PORT = 587

def send_birthday_email(recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
        print(f'Email sent sucessfully')
    except Exception as e:
        print(f'Failed to send email: {e}')

recipient = 'anisiobinzubechi@gmail.com'
subject = 'Birthday Reminder!'

for index, row in df.iterrows():
    birthdate = row['BIRTHDATE(REGULARIZED)']
    name = row['YOUR FULL NAME ']
    
    if birthdate.month == t.month and birthdate.day == t.day:
        print(f"Today is {name}'s birthday!")
        body = f"Today is {name}'s birthday!"
        
        send_birthday_email (recipient, subject, body)
