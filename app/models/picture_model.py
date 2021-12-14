from app.configs.database import db
from dataclasses import dataclass


@dataclass
class PictureModel(db.Model):
    picture_url: str

    __tablename__ = 'pictures'

    id = db.Column(db.Integer, primary_key = True)
    picture_url = db.Column(db.String, nullable = False)
    rep_id = db.Column(db.Integer, db.ForeignKey('republics.id'))
