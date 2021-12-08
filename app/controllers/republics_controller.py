from flask import request
from flask.json import jsonify
from app.models.republic_model import RepublicModel
from app.configs.database import db
from app.controllers.address_controller import create_address

session = db.session

def create_republic():
    republic_data = request.get_json()
    address_data = republic_data.pop("address")

    republic_data["address_id"] = create_address(address_data)
    republic = RepublicModel(**republic_data)
    session.add(republic)
    session.commit()
    return jsonify(republic)


def update_republic():
    ...


def get_all_republics():
    republics = RepublicModel.query.all()
    return jsonify(republics)


def delete_republic():
    ...
