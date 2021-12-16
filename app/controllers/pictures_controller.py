from flask import request, current_app, jsonify
from werkzeug.exceptions import LengthRequired, NotFound
from app.exc.exc import BadRequestError, NonAuthorizedError
from app.models.picture_model import PictureModel
from app.models.republic_model import RepublicModel
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt
from . import verification


@jwt_required(locations=["headers"])
def delete_picture(republic_id, img_id):
    query = PictureModel.query.filter_by(id=img_id).first_or_404()
    republic = RepublicModel.query.filter_by(id=republic_id).first()

    token_data = get_jwt()
    user_email = token_data['sub']['email']
   

    if user_email != republic.user_email:
        return {"error": "only the owner can update the republic"}, 401

    try:
        if republic_id == query.rep_id:
            current_app.db.session.delete(query)
            current_app.db.session.commit()

            date_time =  { "updated_at": datetime.now()}
            for key, value in date_time.items():
                setattr(republic, key, value)
            
            current_app.db.session.commit()
            return '',204
        raise NonAuthorizedError
    except NonAuthorizedError:
        return {"Error": "Non Authorized"},401
    except NotFound:
        return {"Error": "Img not Found"}


@jwt_required(locations=["headers"])
def patch_picture(republic_id, img_id):
    keys = {"picture_url": str}

    query = PictureModel.query.filter_by(id=img_id).first_or_404()
    republic = RepublicModel.query.filter_by(id=republic_id).first()

    token_data = get_jwt()
    user_email = token_data['sub']['email']
   

    if user_email != republic.user_email:
        return {"error": "only the owner can update the republic"}, 401

    try:
        if republic_id == query.rep_id:
            data = request.get_json()
            verification(data, keys)
            if len(data) > 1: raise LengthRequired
            data['picture_url']
            for key, value in data.items():
                setattr(query,key,value)
            date_time =  { "updated_at": datetime.now()}
            for key, value in date_time.items():
                setattr(republic, key, value)
            current_app.db.session.commit()
            return {"picture_url" : data['picture_url']}
        raise NonAuthorizedError
    except NotFound:
        return {"msg": "Img not Found"},404
    except NonAuthorizedError:
        return {"msg": "Non Authorized"},401
    except KeyError:
        return {"msg": "Must have picture_url data"},400
    except LengthRequired:
        return {"msg" "Only picture_url must be in json"},400 
    except BadRequestError as err:
        return jsonify({"error": err.msg}), err.code 
 