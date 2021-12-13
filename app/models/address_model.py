from dataclasses import dataclass
from app.configs.database import db

@dataclass
class AddressModel(db.Model):
    street: str
    street_number: str
    city: str
    zip_code: str
    uf: str

    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    street_number = db.Column(db.String(5), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(8))
    uf = db.Column(db.String(2))
