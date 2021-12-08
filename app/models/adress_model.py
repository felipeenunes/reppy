from dataclasses import dataclass
from app.configs.database import db
@dataclass
class AdressModel(db.Model):
    id: int
    city: str
    street: str
    street_number: str
    zip_code: str
    uf_id: int

    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    street_number = db.Column(db.String(5), nullable=False)
    zip_code = db.Column(db.String(8))
    uf_id = db.Column(db.Integer, db.ForeignKey('states.id'))
