from app.configs.database import db
from dataclasses import dataclass


@dataclass
class PictureModel(db.Model):
    id: int
    picture_url: str
    rep_id: int

    __tablename__ = 'pictures'

    id = db.Column(db.Integer, primary_key = True)
    picture_url = db.Column(db.String, nullable = False, unique=True)
    rep_id = db.Column(db.Integer, db.ForeingKey('republic.id'))