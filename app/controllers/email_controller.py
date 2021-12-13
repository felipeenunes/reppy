from flask import request
import smtplib
import email.message


def send_email():

    data = request.get_json()

    print(data["message"])

    msg =   data["message"]


    mail = email.message.Message()
    mail["Subject"] = "outro email"
    mail["From"] = 'contatoreppy@gmail.com'
    password = '@Senha123'
    mail["To"] = data["recipient"]
    mail.add_header("Content_Type", "text/html")
    mail.set_payload(msg)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(mail["From"], password)
    server.sendmail(mail["From"], [mail["To"]], mail.as_string().encode("utf-8"))
    print("email enviado!")
