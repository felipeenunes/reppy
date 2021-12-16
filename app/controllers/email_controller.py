from os import environ
from flask import request
import smtplib
import email.message
from smtplib import SMTPRecipientsRefused
from dotenv import load_dotenv
from flask_jwt_extended import jwt_required, get_jwt
from app.models.user_model import UserModel
from app.models.republic_model import RepublicModel

load_dotenv()


@jwt_required(locations=["headers"])
def send_email():
    
    mail = email.message.Message()
    mail["From"] = environ.get("EMAIL")
    password = environ.get("EMAIL_PASSWORD")
    mail.add_header("Content_Type", "text/html")
    server = smtplib.SMTP(environ.get("SMTP_SERVER"))
    server.starttls()
    server.login(mail["From"], password)
    
    republic_id = request.get_json()["republic_id"]

    try:
        mail = email.message.Message()
        mail["From"] = environ.get("EMAIL")
        password = environ.get("EMAIL_PASSWORD")
        mail.add_header("Content_Type", "text/html")
        server = smtplib.SMTP(environ.get("SMTP_SERVER"))
        server.starttls()
        server.login(mail["From"], password)
        
        republic_id = request.get_json()["republic_id"]

        republic = RepublicModel.query.get(republic_id)
        owner_email = republic.user_email
        owner = UserModel.query.filter_by(email=owner_email).first()
        interested_email = get_jwt()["sub"]["email"]
        interested = UserModel.query.filter_by(email=interested_email).first()
        interested_name = UserModel.query.filter_by(email=interested_email).first().name
        mail["Subject"] = f"{interested_name} quer conversar sobre a vaga em {republic.name}"
        msg =   f"""
                    Olá {owner.name} tudo bem? 

                    {interested_name} está interessado em morar na {republic.name}.

                    Você pode entrar em contato com ele através dos dados abaixo:
                    
                    Whatsapp:   {interested.phone_number}
                    Email:      {interested_email}.

                    Esperamos que dê tudo certo nas negociações e que vocês possam desfrutar de ótimos momentos.

                    Obrigado por usar a Reppy :)
                """

        mail["To"] = owner_email
        mail.set_payload(msg)
        server.sendmail(mail["From"], [mail["To"]], mail.as_string().encode("utf-8"))

        mail = email.message.Message()
        mail["From"] = environ.get("EMAIL")
        password = environ.get("EMAIL_PASSWORD")
        mail.add_header("Content_Type", "text/html")
        server = smtplib.SMTP(environ.get("SMTP_SERVER"))
        server.starttls()
        server.login(mail["From"], password)
        
        republic_id = request.get_json()["republic_id"]

        msg = f"""
            Olá {interested.name}, tudo bem?

            Seu interesse em morar em {republic.name} já foi enviado para {owner.name} e logo que possível ele deverá entrar em contato com você para acertarem os detalhes.

            Esperamos que tudo dê certo e que você tenha uma experiência incrível na sua nova moradia.

            Obrigado por usar a Reppy :)
            """

        mail["Subject"] = f"Confirmação de interesse - {republic.name}"
        mail["To"] = interested.email
        mail.set_payload(msg)
        server.sendmail(mail["From"], [mail["To"]], mail.as_string().encode("utf=8"))
        return {"msg": "email sent"}
    except SMTPRecipientsRefused:
        return {"msg": "error when sending email"}, 400
