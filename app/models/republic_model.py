from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy.orm import backref
from app.models.address_model import AddressModel
from app.models.picture_model import PictureModel
from app.models.user_model import UserModel

@dataclass
class RepublicModel(db.Model):
    
    id: int
    name: str
    description: str
    vacancies_qty: int
    max_occupancy: int
    price: float
    created_at: db.DateTime
    updated_at: db.DateTime
    address: AddressModel
    pictures: PictureModel
    user: UserModel

    __tablename__ = "republics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String, default='')
    vacancies_qty = db.Column(db.Integer, nullable=False)
    max_occupancy = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    user_cpf = db.Column(db.String, db.ForeignKey('users.cpf'))
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), unique=True)

    address = db.relationship('AddressModel', backref = backref('republic', uselist = False), uselist = False, cascade='all, delete-orphan', single_parent=True)
    pictures = db.relationship('PictureModel', backref = backref('republic', uselist = False), uselist = True, cascade='all, delete-orphan', single_parent=True)
    user = db.relationship('UserModel', backref = backref('republic', uselist = True), uselist = False)