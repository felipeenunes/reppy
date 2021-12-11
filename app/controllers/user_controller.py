from flask import request, current_app, jsonify
from sqlalchemy.orm import query
from werkzeug.exceptions import NotFound
from app.models.user_model import UserModel
from app.controllers.address_controller import create_address,address_delete, update_adress
from app.exc.exc import InvalidKeys, MissingKeys, PhoneError,InvalidQuantityPassword,KeyErrorUser,EmailError
from sqlalchemy.exc import IntegrityError, ProgrammingError
from psycopg2.errors import UniqueViolation, NotNullViolation, SyntaxError
import re
from flask_jwt_extended import create_access_token,get_jwt,jwt_required

def create_user():
    try:
        data = request.get_json()
        data['phone_number']= str(data['phone_number'])
        data["password"] = str(data["password"] )

        keys = {"cpf","name","email","email","college","phone_number","password", "address"}
        extra_keys = set(data.keys()).difference(keys)
        if extra_keys:
                raise InvalidKeys(','.join(list(extra_keys)))

        if len(data['password']) < 6:
           raise InvalidQuantityPassword('Password must contain at least 6 digits')
        
       
        data_address = data.pop("address")
        
        data['address_id'] = create_address(data_address)
        
        user = UserModel(**data)
        current_app.db.session.add(user)
        current_app.db.session.commit()
        
        return jsonify(user), 201
    except ValueError:
        address_delete(data['address_id'])
        return {"error":"Field cpf must have 11 characters"},400
    except PhoneError as err:
        address_delete(data['address_id'])
        return jsonify({'error':str(err)}),400
    except IntegrityError as e: 
        if isinstance(e.orig, NotNullViolation):
            current_app.db.session.rollback()
            address_delete(data['address_id'])
            return {"error": "missing keys"}, 400
        if isinstance(e.orig, UniqueViolation):
            current_app.db.session.rollback()
            address_delete(data['address_id'])
            return jsonify({'error':'cpf, email or name already exists'}),409
    except TypeError as e:
        return jsonify({"error":"values must be strings"}),400
    except InvalidKeys as e:
        return {"msg": f"invalid keys: {e}"}, 400
    except InvalidQuantityPassword as e:
        return jsonify({'error': str(e)}),400
    except KeyErrorUser as e:
        return jsonify({'error': f'keys must contain{str(e)}'}),400
    except EmailError as e:
        return jsonify({'error':str(e)}),400
    except MissingKeys as e:
        return {'error': f'missing the following keys: {e}'}, 400


def login_user():

    data = request.get_json()

    try:
        if 'email' in data and 'password' in data and len(data) == 2:
            user = UserModel.query.filter_by(email=data['email']).first()
            if user is None:
                    raise KeyErrorUser('User not found')
            if user.check_password(data['password']):
                access_token = create_access_token(user)
                return jsonify({'token': access_token}),200
            
            return jsonify({'Error':'Email and password incorrect'}),401
        else : raise KeyError
    except KeyError:
        return jsonify({'Error':'Email and password must be given only'}),400
    except KeyErrorUser as e:
            return jsonify({'Error':str(e)}),404




@jwt_required(locations=["headers"])
def update_user():
        data = request.json
        email_token = get_jwt()
        try:
                
                user = UserModel.query.filter_by(email=email_token['sub']['email']).first_or_404()
                output = {}
                for i in data:
                        if type(data[i]) != str and i != 'address':
                                raise TypeError
                #if 'cpf' in data: del data['cpf']
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

                user.query.filter_by(email=email_token['sub']['email']).update(output)
                current_app.db.session.commit()
               
                if 'password' in data:
                        output.pop('password_hash')
             
                return jsonify(user), 202
        
        except AttributeError:
                return {"error": "invalid UF, try XX"},400
        except NotFound:
                return {"error": "user not found"},404
        except TypeError:
                return {"error": "all data must be string, except address"},400
        except PhoneError:
                return {"error": "incorrect, correct phone format:(xx)xxxxx-xxxx!"}, 400
        except (UniqueViolation, IntegrityError):
                return jsonify({'error':'cpf, email ou name already exists'}),409
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
