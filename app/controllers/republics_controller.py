from datetime import datetime
from flask import request, current_app, jsonify
from flask.json import jsonify
from sqlalchemy.exc import IntegrityError, DataError
from app.exc.exc import BadRequestError, NotFoundError, InvalidZipCode
from app.models.republic_model import RepublicModel
from app.models.picture_model import PictureModel
from app.configs.database import db
from app.controllers.address_controller import create_address, update_addresses_from_rep
from datetime import datetime

def create_republic():
    try:
        session = current_app.db.session
        data = request.get_json()
        required_keys = ["name", "description", "price", "vacancies_qty", "max_occupancy", "pictures", "address", "user_cpf"]
        new_data = {}
        for key in required_keys:
            if not key in data:
                raise BadRequestError("Required keys not satisfied")
            new_data[key] = data[key]
        pictures = new_data.pop('pictures')
        address = new_data.pop('address')
        new_data['address_id'] = create_address(address)
        new_data['created_at'] = datetime.now()
        new_data['updated_at'] = datetime.now()
        republic = RepublicModel(**new_data)
        session.add(republic)
        session.flush()
        pictures_list = []
        for pic in pictures:
            pic['rep_id']=republic.id
            new_pic = PictureModel(**pic)
            session.add(new_pic)
            added_picture = PictureModel.query.filter_by(picture_url=pic['picture_url']).first()
            pictures_list.append(added_picture)
        session.commit()
        return jsonify({
            "id": republic.id,
            "user_cpf": republic.user_cpf,
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

def update_republic(id):
    ...


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
