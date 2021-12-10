from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy.orm import validates
import re
from app.exc.exc import EmailError, PhoneError
from werkzeug.security import generate_password_hash,check_password_hash,gen_salt

from sqlalchemy.orm import backref

@dataclass
class UserModel(db.Model):

    name:str
    email:str
    college:str
    phone_number:str

    __tablename__ = 'users'

    #region properties

    cpf = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    college = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))

    address = db.relationship('AddressModel',backref= backref('address',uselist = True))

    @property
    def password(self):
        raise AttributeError("Password can't be empty")
    
    @password.setter
    def password(self, password_to_hash):
        salt = gen_salt(16)
        self.password_hash = generate_password_hash(password_to_hash)

    #endregion

    #region validations
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

    @validates('email')
    def validates_email(self,_,email):
        regex = r"^[\w-]+@[a-z\d]+\.[\w]{3}"
        match = re.fullmatch(regex,email)
        if not match:
            raise EmailError("user@email.com")
        return email
    
    #endregion

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)

