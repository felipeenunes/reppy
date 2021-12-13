from datetime import datetime
from flask import request, current_app, jsonify
from flask.json import jsonify
from sqlalchemy.exc import IntegrityError
from app.exc.exc import BadRequestError, NotFoundError, InvalidZipCode
from app.models.republic_model import RepublicModel
from app.models.picture_model import PictureModel
from app.configs.database import db
from app.controllers.address_controller import create_address, update_adress
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt

from app.models.user_model import UserModel


@jwt_required(locations=["headers"])
def create_republic():
    try:
        session = current_app.db.session
        data = request.get_json()
        user_token = get_jwt()
        user_email = user_token['sub']['email']
        user = UserModel.query.filter_by(email=user_email).first()
        data['user_email'] = user.email
        new_data = RepublicModel.verify_keys(data)
        pictures = new_data.pop('pictures')
        address = new_data.pop('address')
        new_data['address_id'] = create_address(address)
        republic = RepublicModel(**new_data)
        session.add(republic)
        session.flush()
        pictures_list = RepublicModel.create_pictures_list(pictures, session, republic.id)
        session.commit()
        print(republic)
        return jsonify({
            "id": republic.id,
            "user_email": republic.user_email,
            "name": republic.name,
            "description": republic.description,
            "vacancies_qty": republic.vacancies_qty,
            "max_occupancy": republic.max_occupancy,
            "price": republic.price,
            "created_at": republic.created_at,
            "update_at": republic.updated_at,
            "address_id": republic.address_id,
            "pictures": pictures_list,
        })
    except IntegrityError:
        return jsonify({"error": "User not found"}), 400
    except BadRequestError as err:
        return jsonify({"error": err.msg}), err.code
    except InvalidZipCode as e:
        return {'error': str(e)}, 400

@jwt_required(locations=["headers"])
def update_republic(republic_id):
    republic = RepublicModel.query.get(republic_id)
    owner = UserModel.query.filter_by(cpf = republic.user_cpf).first()
    print(republic, '\n\n\n\n', owner)

    token_data = get_jwt()
    user_email = token_data['sub']['email']
    print('\n\n\n\n', user_email)

    if user_email != owner.email:
        return {"error": "only the owner can update the republic"}, 401


    update_data = request.json

    if 'address' in update_data:
        new_address = update_data.pop('address')
        update_adress(new_address, republic.address.id)

    update_data['updated_at'] = datetime.now()

    updated_republic = RepublicModel.query.filter_by(id = republic_id).update(update_data)
    current_app.db.session.commit()

    updated_republic = RepublicModel.query.get(republic_id)

    return jsonify(updated_republic), 200


def get_all_republics():
    republics = RepublicModel.query.all()
    return jsonify(republics)

def get_one(id: int):
    try:
        republic = RepublicModel.query.get(id)
        if not republic:
            raise IndexError
    except IndexError:
        return {'Error': 'republic not found'}, 404
    return jsonify(republic)

def delete_republic(id: int):
    try:
        session = current_app.db.session
        republic = RepublicModel.query.get(id)
        if not republic:
            raise NotFoundError("Republic not found.")
        session.delete(republic)
        session.commit()
        return {}, 204
    except NotFoundError as err:
        return jsonify({"error": err.msg}), err.code
