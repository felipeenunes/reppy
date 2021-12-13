from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy.orm import backref
from app.models.address_model import AddressModel
from app.models.picture_model import PictureModel
from app.models.user_model import UserModel
from app.exc.exc import BadRequestError
from datetime import datetime

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

    __tablename__ = "republics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String, default='')
    vacancies_qty = db.Column(db.Integer, nullable=False)
    max_occupancy = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    user_email = db.Column(db.String, db.ForeignKey('users.email'))
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), unique=True)

    address = db.relationship('AddressModel', backref = backref('republic', uselist = False), uselist = False, cascade='all, delete-orphan', single_parent=True)
    pictures = db.relationship('PictureModel', backref = backref('republic', uselist = False), uselist = True, cascade='all, delete-orphan', single_parent=True)
    user = db.relationship('UserModel', backref = backref('republic', uselist = True), uselist = False)
    
    @staticmethod
    def verify_keys(data):
        required_keys = ["name", "description", "price", "vacancies_qty", "max_occupancy", "pictures", "address", "user_email"]
        new_data = {}
        for key in required_keys:
            if not key in data:
                raise BadRequestError("Required keys not satisfied")
            new_data[key] = data[key]
        new_data['created_at'] = datetime.now()
        new_data['updated_at'] = datetime.now()
        return new_data
        
    @staticmethod
    def create_pictures_list(pictures, session, id):
        pictures_list = []
        for pic in pictures:
            pic['rep_id']=id
            new_pic = PictureModel(**pic)
            session.add(new_pic)
            added_picture = PictureModel.query.filter_by(picture_url=pic['picture_url']).first()
            pictures_list.append(added_picture)
        return pictures_list