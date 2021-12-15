from datetime import datetime
from flask import request, current_app, jsonify
from flask.json import jsonify
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from app.exc.exc import BadRequestError, NotFoundError
from app.models.republic_model import RepublicModel
from app.controllers.address_controller import create_address, update_adress
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt
from app.models.user_model import UserModel
from app import controllers
from app.controllers.extra_controller import create_extra


@jwt_required(locations=["headers"])
def create_republic():
    try:
        session = current_app.db.session
        data = request.get_json()
        required_keys = {"name":str, "description":str, "price":int, "vacancies_qty":int, "max_occupancy":int, "pictures":list, "address":dict}
        controllers.verification(data, required_keys)
        user_token = get_jwt()
        user_email = user_token['sub']['email']

        user = UserModel.query.filter_by(email=user_email).first()
        data['user_email'] = user.email

        new_data = RepublicModel.verify_keys(data)
        pictures = new_data.pop('pictures')
        address = new_data.pop('address')
        new_data['address_id'] = create_address(address)
        extras = new_data.pop('extras')
        republic = RepublicModel(**new_data)
        
        extras['republic_id'] = republic.id
        extra_model = create_extra(extras)

        session.add(republic)
        session.flush()
        pictures_list = RepublicModel.create_pictures_list(pictures, session, republic.id)
        session.commit()
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


@jwt_required(locations=["headers"])
def update_republic(republic_id):
    try: 
        republic = RepublicModel.query.get(republic_id)
        owner = UserModel.query.filter_by(email = republic.user_email).first()
        

        token_data = get_jwt()
        user_email = token_data['sub']['email']
    

        if user_email != owner.email:
            return {"error": "only the owner can update the republic"}, 401

        update_data = request.json
        keys = {"name":str, "description":str, "price":int, "vacancies_qty":int, "max_occupancy":int, "pictures":list, "address":dict}
        required_keys = {key:value for key,value in keys.items() if key in update_data}
 
        controllers.verification(update_data, required_keys)

        if 'address' in update_data:
            new_address = update_data.pop('address')
            update_adress(new_address, republic.address.id)

        update_data['updated_at'] = datetime.now()

        updated_republic = RepublicModel.query.filter_by(id = republic_id).update(update_data)
        current_app.db.session.commit()

        updated_republic = RepublicModel.query.get(republic_id)

        return jsonify(updated_republic), 200
    except BadRequestError as err:
        return jsonify({"error": err.msg}), err.code
    except InvalidRequestError:
        return {"msg": "invalid keys to be updated"}, 400
    except AttributeError:
        return {"msg": "republic not found"}, 404


def get_all_republics():
    args_dict = {}
    args = request.args
    for i in args:
        args_dict[i] = args[i]
    if 'min_price' not in args_dict: args_dict["min_price"] = 0
    if 'max_price' not in args_dict: args_dict["max_price"] = 10000
    if 'max_residence' not in args_dict: args_dict["max_residence"] = 1000
    if 'uf' not in args_dict: args_dict['uf'] = ''
    
    republics = RepublicModel.query.filter(RepublicModel.price <= args_dict['max_price']).filter(RepublicModel.price >= args_dict['min_price']).filter(RepublicModel.vacancies_qty <= args_dict["max_residence"]).all()
    republics = controllers.filter_by_uf(republics,args_dict['uf'])
    
    if len(republics):
        return jsonify(republics),200
    else:
        return jsonify([])
    

def get_one(id: int):
    try:
        republic = RepublicModel.query.get(id)
        if not republic:
            raise IndexError
    except IndexError:
        return {'Error': 'republic not found'}, 404
    return jsonify(republic)


@jwt_required(locations=["headers"])
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
