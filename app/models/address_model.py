from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy.orm import backref
from app.models.state_model import StateModel

@dataclass
class AddressModel(db.Model):
    street: str
    street_number: str
    zip_code: str
    city: str
    state: str

    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    street_number = db.Column(db.String(5), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    uf_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    zip_code = db.Column(db.String(8))

    state = db.relationship('StateModel', backref = backref('address', uselist = True), uselist = False)
