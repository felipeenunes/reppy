from datetime import datetime
from flask import request, current_app, jsonify
from flask.json import jsonify
from app.models.republic_model import RepublicModel
from app.models.picture_model import PictureModel
from app.configs.database import db

def create_republic():
    session = current_app.db.session
    data = request.get_json()
    pictures = data.pop('pictures')
    data['created_at'] = datetime.now()
    data['updated_at'] = datetime.now()

    republic = RepublicModel(**data)
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
        "name": republic.name,
        "description": republic.description,
        "price": republic.price,
        "vacancies_qty": republic.vancancies_qty,
        "max_occupancy": republic.max_occupancy,
        "created_at": republic.created_at,
        "updated_at": republic.updated_at,
        "pictures": pictures_list,
    })




def update_republic():
    ...


def get_all_republics():
    republics = RepublicModel.query.all()
    return jsonify(republics)


def delete_republic():
    ...
