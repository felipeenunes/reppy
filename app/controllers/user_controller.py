from flask import request, current_app, jsonify
from werkzeug.exceptions import NotFound
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
        
        return jsonify({"cpf":user.cpf,"name": user.name, "email":user.email, "college":user.college,"phone_number":user.phone_number, "address":user.address}), 201
    except ValueError:
        address_get(data['address_id'])
        return {"Error":"Field cpf must have 11 characters"},400
    except PhoneError as err:
        address_get(data['address_id'])
        return jsonify({'Erro':str(err)}),400
    except (UniqueViolation, IntegrityError):
        current_app.db.session.rollback()
        address_get(data['address_id'])
        return jsonify({'Error':'cpf, email ou name already exists'}),409
    except AttributeError:
        return jsonify({"Error": "values must be strings"})


def login_user():

    data = request.get_json()

    try:
        if 'email' in data and 'password' in data and len(data) == 2:
            user = UserModel.query.filter_by(email=data['email']).first()
            
            if user.check_password(data['password']):
                return jsonify({'passou':'passou'}),200
            
            return jsonify({'Error':'Email and password incorrect'}),401
        else : raise KeyError
    except KeyError:
        return jsonify({'Error':'Email and password must be given only'}),400

def update_user():
    ...


def get_user_by_id(cpf):
        try:
                
                query = UserModel.query.filter_by(cpf=cpf).first_or_404()
                return jsonify(query),200

        except NotFound:
                return {"Error": "User not Found"},404

# discutir necessidade
def delete_user(cpf):
        try:
                query = UserModel.query.filter_by(cpf=cpf).first_or_404()
                current_app.db.session.delete(query)
                current_app.db.session.commit()
                return '', 204
        except NotFound:
                return {"Error": "User not Found"},404

