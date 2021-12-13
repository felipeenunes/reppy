from os import environ
from flask import request
import smtplib
import email.message
from smtplib import SMTPRecipientsRefused
from dotenv import load_dotenv

load_dotenv()

def send_email():

    try:
        data = request.get_json()

        print(data["message"])

        msg =   data["message"]


        mail = email.message.Message()
        mail["Subject"] = data["subject"]
        mail["From"] = environ.get("EMAIL")
        password = environ.get("EMAIL_PASSWORD")
        mail["To"] = data["recipient"]
        mail.add_header("Content_Type", "text/html")
        mail.set_payload(msg)

        server = smtplib.SMTP(environ.get("SMTP_SERVER"))
        server.starttls()
        server.login(mail["From"], password)
        server.sendmail(mail["From"], [mail["To"]], mail.as_string().encode("utf-8"))
        return {"msg": "email sent"}
    except SMTPRecipientsRefused:
        return {"msg": "error when sending email"}, 400

    
