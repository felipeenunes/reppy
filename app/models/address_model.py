from dataclasses import dataclass
from app.configs.database import db
@dataclass
class AddressModel(db.Model):
    id: int
    street: str
    street_number: str
    city: str
    uf_id: int
    zip_code: str

    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    street_number = db.Column(db.String(5), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    uf_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    zip_code = db.Column(db.String(8))
