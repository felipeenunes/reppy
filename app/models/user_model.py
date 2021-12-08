from dataclasses import dataclass
from app.configs.database import db

@dataclass
class UserModel(db.Model):

    cpf:str
    name:str
    email:str
    college:str
    phone_number:str
    password:str

    __tablename__ = 'users'

    cpf = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    college = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    adress_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))
