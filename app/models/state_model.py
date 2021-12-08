from dataclasses import dataclass
from app.configs.database import db

@dataclass
class StateModel(db.Model):

    id: int
    uf: str

    __tablename__ = "state"

    id = db.Column(db.Integer, primary_key=True)
    uf = db.Column(db.String(2), nullable=False)
