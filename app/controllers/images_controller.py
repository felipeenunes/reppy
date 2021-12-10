from flask import request, current_app
from werkzeug.exceptions import LengthRequired, NotFound
from app.exc.exc import NonAuthorizedError
from app.models.picture_model import PictureModel

def delet_picture_img(republic_id, img_id):
    query = PictureModel.query.filter_by(id=img_id).first_or_404()
    try:
        if republic_id == query.rep_id:
            current_app.db.session.delete(query)
            current_app.db.session.commit()
            return '',204
        raise NonAuthorizedError
    except NonAuthorizedError:
        return {"Error": "Non Authorized"},401
    except NotFound:
        return {"Error": "Img not Found"}

def patch_picture_img(republic_id, img_id):
    query = PictureModel.query.filter_by(id=img_id).first_or_404()
    
    try:
        if republic_id == query.rep_id:
            data = request.get_json()
            if len(data) > 1: raise LengthRequired
            data['picture_url']
            for key, value in data.items():
                setattr(query,key,value)
            current_app.db.session.commit()
            return {"picture_url" : data['picture_url']}
        raise NonAuthorizedError
    
    except NonAuthorizedError:
        return {"Error": "Non Authorized"},401
    except NotFound:
        return {"Error": "Img not Found"},404
    except KeyError:
        return {"Error": "Must have picture_url data"},400
    except LengthRequired:
        return {"Error" "Only picture_url must be in json"},400