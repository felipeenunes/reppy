from flask import request
from flask.json import jsonify
from app.models.republic_model import RepublicModel
from app.configs.database import db

def create_republic():
    data = request.get_json()
    
    republic = RepublicModel(**data)
    db.session.add(republic)
    db.session.commit()




def update_republic():
    ...


def get_all_republics():
    republics = RepublicModel.query.all()
    return jsonify(republics)


def delete_republic():
    ...
