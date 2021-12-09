from flask import request, current_app, jsonify
from werkzeug.exceptions import NotFound
from app.models.user_model import UserModel
from app.controllers.address_controller import create_address
from app.exc.exc import PhoneError,InavlidQuantyPassword
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from app.models.address_model import AddressModel
from flask_jwt_extended import create_access_token

def address_get(address):
    address = AddressModel.query.get(address)
    current_app.db.session.delete(address)
    current_app.db.session.commit()

def create_user():
    try:
        data = request.get_json()

        data_address = data.pop("address")
        
        data['address_id'] = create_address(data_address)

        if len(data['password']) < 6:
           raise InavlidQuantyPassword('Password must contain at least 6 digits')

        
        user = UserModel(**data)
        current_app.db.session.add(user)
        current_app.db.session.commit()
        
        return jsonify({"cpf":user.cpf,"name": user.name, "email":user.email, "college":user.college,"phone_number":user.phone_number, "address":user.address}), 201
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
    except AttributeError:
        return jsonify({"error": "values must be strings"})
    except InavlidQuantyPassword as e:
        return jsonify({'error': str(e)})


def login_user():

    data = request.get_json()

    try:
        if 'email' in data and 'password' in data and len(data) == 2:
            user = UserModel.query.filter_by(email=data['email']).first()
            
            if user.check_password(data['password']):
                access_token = create_access_token(user)
                return jsonify({'token': access_token}),200
            
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
                return {"msg": "User not Found"},404

# discutir necessidade
def delete_user(cpf):
        try:
                query = UserModel.query.filter_by(cpf=cpf).first_or_404()
                current_app.db.session.delete(query)
                current_app.db.session.commit()
                return '', 204
        except NotFound:
                return {"msg": "User not Found"},404

