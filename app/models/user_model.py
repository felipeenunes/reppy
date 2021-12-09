from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy.orm import backref, validates

@dataclass
class UserModel(db.Model):

    name:str
    email:str
    college:str
    phone_number:str

    __tablename__ = 'users'

    cpf = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    college = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))

    @validates('cpf')
    def validate_cpf(self,_,cpf):
        if len(cpf) != 11 or not cpf.isnumeric():
            raise ValueError
        return cpf
