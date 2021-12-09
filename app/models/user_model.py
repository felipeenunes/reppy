from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy.orm import validates
import re
from app.exc.exc import PhoneError
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.orm import backref

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
    password_hash = db.Column(db.String, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))

    address = db.relationship('AddressModel',backref= backref('address',uselist = True))

    @validates('cpf')
    def validate_cpf(self,_,cpf):
        if len(cpf) != 11 or not cpf.isnumeric():
            raise ValueError
        return cpf
    
    @validates('phone_number')
    def validate_phone(self,_,phone):
        regex = r"\([1-9]\d\)\s?\d{5}-\d{4}"
        match = re.fullmatch(regex,phone)
        if not match:
            raise PhoneError("Incorrect, correct phone format:(xx)xxxxx-xxxx!")
        return phone
    
    @property
    def password(self):
        raise AttributeError("Password can't be empty")
    
    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)
    
    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)

