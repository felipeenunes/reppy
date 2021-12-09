from flask import jsonify, request, current_app
from app.models.user_model import UserModel
from app.controllers.address_controller import create_address
from app.exc.exc import PhoneError
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from app.models.address_model import AddressModel

def address_get(address):
    address = AddressModel.query.get(address)
    current_app.db.session.delete(address)
    current_app.db.session.commit()

def create_user():
    try:
        data = request.get_json()

        data_address = data.pop("address")
        
        data['address_id'] = create_address(data_address)
        
        user = UserModel(**data)
        current_app.db.session.add(user)
        current_app.db.session.commit()
        
        return jsonify(user), 201
    except ValueError:
        address_get(data['address_id'])
        return {"error":"Field cpf must have 11 characters"},400
    except PhoneError as err:
        address_get(data['address_id'])
        return jsonify({'Erro':str(err)}),400
    except (UniqueViolation, IntegrityError):
        current_app.db.session.rollback()
        address_get(data['address_id'])
        return jsonify({'Error':'cpf, email ou name already exists'}),409
    





def update_user():
    ...


# discutir necessidade
def get_user():
    ...


# discutir necessidade
def delete_user():
    ...
