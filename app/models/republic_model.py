from sqlalchemy.sql.expression import update
from app.configs.database import db
from app.models.user_model import UserModel
from dataclasses import dataclass

@dataclass
class RepublicModel(db.Model):
    
    id: int
    name: str
    description: str
    vancancies_qty: int
    max_occupancy: int
    price: float
    created_at: db.DateTime
    updated_at: db.DateTime

    __tablename__ = "republic"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String, default='')
    vancancies_qty = db.Column(db.Integer, nullable=False)
    max_occupancy = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    student_cpf = db.Column(db.String, db.ForeignKey(user.cpf))
    address_id = db.Column(db.Integer, db.ForeignKey(address.id))
    extras_id = db.Column(db.Integer, db.ForeignKey(extras.id))