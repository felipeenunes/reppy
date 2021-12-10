from flask import request, current_app, jsonify
from sqlalchemy.orm import query
from werkzeug.exceptions import NotFound
from app.models.user_model import UserModel
from app.controllers.address_controller import create_address,address_delete, update_adress
from app.exc.exc import PhoneError,InavlidQuantyPassword,KeyErrorUser,EmailErro
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
import re
from flask_jwt_extended import create_access_token


def create_user():
    try:
        data = request.get_json()

        keys = ["cpf","name","email","email","college","phone_number","password", "address"]
        for key in keys:
            if not key in data: 
                raise KeyErrorUser("Key must be cpf,name,email,phone_number,password")

        if len(data['password']) < 6:
           raise InavlidQuantyPassword('Password must contain at least 6 digits')
        
       
        data_address = data.pop("address")
        
        data['address_id'] = create_address(data_address)
        
        user = UserModel(**data)
        current_app.db.session.add(user)
        current_app.db.session.commit()
        
        return jsonify({"cpf":user.cpf,"name": user.name, "email":user.email, "college":user.college,"phone_number":user.phone_number, "address":user.address}), 201
    except ValueError:
        address_delete(data['address_id'])
        return {"error":"Field cpf must have 11 characters"},400
    except PhoneError as err:
        address_delete(data['address_id'])
        return jsonify({'Erro':str(err)}),400
    except (UniqueViolation, IntegrityError):
        current_app.db.session.rollback()
        address_delete(data['address_id'])
        return jsonify({'Error':'cpf, email ou name already exists'}),409
    except AttributeError:
        return jsonify({"error": "values must be strings"})
    except InavlidQuantyPassword as e:
        return jsonify({'error': str(e)}),400
    except KeyErrorUser as e:
        return jsonify({'error': str(e) }),400
    except EmailErro as e:
        return jsonify({'error':str(e)}),200


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

def update_user(cpf):
        data = request.json
        try:
                user = UserModel.query.filter_by(cpf=cpf).first_or_404()
                output = {}
                for i in data:
                        if type(data[i]) != str and i != 'address':
                                raise TypeError
                if 'cpf' in data: del data['cpf']
                if 'name' in data: output['name'] = data['name']
                if 'email' in data: output['email'] = data['email']
                if 'college' in data: output['college'] = data['college']
                if 'phone_number' in data:
                        regex = r"\([1-9]\d\)\s?\d{5}-\d{4}"
                        match = re.fullmatch(regex,data['phone_number'])
                        if not match:
                            raise PhoneError("Incorrect, correct phone format:(xx)xxxxx-xxxx!")
                        output['phone_number'] = data['phone_number']
                        
                if 'password' in data:
                     user.password = data['password']
                     output['password_hash'] = user.password_hash
                for key, value in data.items():
                        setattr(query,key,value)
                if 'address' in data:
                        output['adress'] = update_adress(data['address'], query)
                user.query.filter_by(cpf=cpf).update(output)
                current_app.db.session.commit()
                output.pop('password_hash')
                return output, 202
        
        except AttributeError:
                return {"msg": "Invalid UF, try XX"},400
        except NotFound:
                return {"msg": "User not found"},404
        except TypeError:
                return {"msg": "All data must be string, except address"},400
        except PhoneError:
                return {"msg": "Incorrect, correct phone format:(xx)xxxxx-xxxx!"}, 400
        except (UniqueViolation, IntegrityError):
                return jsonify({'Error':'cpf, email ou name already exists'}),409


def get_user_by_id(cpf):
        try:
                query = UserModel.query.filter_by(cpf=cpf).first_or_404()
                return jsonify(query),200

        except NotFound:
                return {"msg": "User not Found"},404


def delete_user(cpf):
        try:
                query = UserModel.query.filter_by(cpf=cpf).first_or_404()
                current_app.db.session.delete(query)
                current_app.db.session.commit()
                return '', 204
        except NotFound:
                return {"msg": "User not Found"},404
