from app.configs.database import db
from sqlalchemy.orm import backref
from dataclasses import dataclass


@dataclass
class ExtraModel(db.Model):

    __tablename__ = 'extras'

    id = db.Column(db.Integer, primary_key = True)
    animals_allowed = db.Column(db.Boolean, nullable = False)
    parties_allowed = db.Column(db.Boolean, nullable = False)
    wifi = db.Column(db.Boolean, nullable = False)
    swiming_pool = db.Column(db.Boolean, nullable = False)
    grill = db.Column(db.Boolean, nullable = False)
    republic_id = db.Column(db.Integer, db.ForeignKey('republics.id'), unique = True)

    republic = db.relationship('RepublicModel', backref = backref('extra', uselist = False, cascade = 'all, delete-orphan'), uselist = False)