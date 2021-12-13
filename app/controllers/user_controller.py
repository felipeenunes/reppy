from flask import request, current_app, jsonify
from sqlalchemy.orm import query
from werkzeug.exceptions import NotFound
from app.models.user_model import UserModel
from app.controllers.address_controller import create_address,address_delete, update_adress
from app.exc.exc import KeyErrorUser,BadRequestError,NotFoundError,BadRequestWithDeleteError
from sqlalchemy.exc import IntegrityError, ProgrammingError
from psycopg2.errors import UniqueViolation, NotNullViolation, SyntaxError
import re
from flask_jwt_extended import create_access_token,get_jwt,jwt_required

def create_user():
    try:
        data = request.get_json()
        data['phone_number']= str(data['phone_number'])
        data["password"] = str(data["password"] )
        required_keys = {"cpf","name","email","college","phone_number","password", "address"}
        new_data={}
        missing_keys=[]
        for key in required_keys:
                if not key in data:
                        missing_keys.append(key)
        if missing_keys: raise BadRequestError(f'Required keys not found: {missing_keys}')
        for key in data:
                if key in required_keys:
                        new_data[key] = data[key]    
        if len(data['password']) < 6:
           raise BadRequestError('Password must contain at least 6 digits')    
        data_address = data.pop("address")
        data['address_id'] = create_address(data_address)
        user = UserModel(**data)
        current_app.db.session.add(user)
        current_app.db.session.commit()
        return jsonify(user), 201
    except BadRequestWithDeleteError as e:
        address_delete(data['address_id'])
        return {"error": e.msg}, e.code
    except IntegrityError as e: 
        if isinstance(e.orig, NotNullViolation):
            current_app.db.session.rollback()
            address_delete(data['address_id'])
            return {"error": "missing keys"}, 400
        if isinstance(e.orig, UniqueViolation):
            current_app.db.session.rollback()
            address_delete(data['address_id'])
            return jsonify({'error':'cpf, email or name already exists'}),409
    except KeyError:
        return jsonify({'Error':'Email and password must be given only'}),400
    except BadRequestError as e:
        return {"error": e.msg}, e.code
  
def login_user():

    data = request.get_json()
    try:
        keys = {"email","password"}
        extra_keys = set(data.keys()).difference(keys)
        if extra_keys:
                raise BadRequestError(f'{",".join(list(extra_keys))}')     
        user = UserModel.query.filter_by(email=data['email']).first()
        if user is None:
                raise KeyErrorUser('User not found')
        if user.check_password(data['password']):
                access_token = create_access_token(user)
                return jsonify({'token': access_token}),200    
        return jsonify({'Error':'Email and password incorrect'}),401
    except KeyError:
        return jsonify({'error':'Email and password must be given only'}),400
    except NotFoundError as e:
            return jsonify({"error": e.msg}), e.code
    except TypeError:
            return  jsonify({'error':'Email and password must be given only'}),400
    except BadRequestError as e:
        return jsonify({"error": e.msg}), e.code

@jwt_required(locations=["headers"])
def update_user():
        data = request.json
        email_token = get_jwt()
        try:
                user = UserModel.query.filter_by(email=email_token['sub']['email']).first_or_404()
                output = {}
                for i in data:
                        if type(data[i]) != str and i != 'address':
                                raise BadRequestError("All data must be string, except address")
                if 'name' in data: output['name'] = data['name']
                if 'email' in data: output['email'] = data['email']
                if 'college' in data: output['college'] = data['college']
                if 'phone_number' in data:
                        regex = r"\([1-9]\d\)\s?\d{5}-\d{4}"
                        match = re.fullmatch(regex,data['phone_number'])
                        if not match:
                            raise BadRequestError("Incorrect format, correct phone format:(xx)xxxxx-xxxx!")
                        output['phone_number'] = data['phone_number']
                        
                if 'password' in data:
                     user.password = data['password']
                     output['password_hash'] = user.password_hash
                for key, value in data.items():
                        setattr(query,key,value)
                if 'address' in data:
                        output['adress'] = update_adress(data['address'], query)

                user.query.filter_by(email=email_token['sub']['email']).update(output)
                current_app.db.session.commit()
               
                if 'password' in data:
                        output.pop('password_hash')
             
                return jsonify(user), 202
        except BadRequestError as err:
                return jsonify({"error": err.msg}), err.code
        except AttributeError:
                return {"error": "invalid UF, try XX"},400
        except NotFound:
                return {"error": "user not found"},404
        except (UniqueViolation, IntegrityError):
                return jsonify({'error':'cpf, email or name already exists'}),409
        except ProgrammingError as e:
                if isinstance(e.orig, SyntaxError):
                        return {"error": "invalid key on update, of attempt to change cpf"}, 422

def get_user_by_id(cpf):
        try:
                query = UserModel.query.filter_by(cpf=cpf).first_or_404()
                return jsonify(query),200

        except NotFound:
                return {"error": "User not Found"},404


@jwt_required(locations=["headers"])
def delete_user():
        email_token = get_jwt()
        try:
                query = UserModel.query.filter_by(email=email_token['sub']['email']).first_or_404()
                current_app.db.session.delete(query)
                current_app.db.session.commit()
                return '', 204
        except NotFound:
                return {"Error": "User not Found"}, 404

