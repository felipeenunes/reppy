from app.models.extras_model import ExtraModel
from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required

def filter_extras_true(extras):
    extras = extras.__dict__
    del extras['_sa_instance_state']
    del extras['id']
    del extras['republic_id']

    extras_list = []
    for key, value in extras.items():
        if value:
            extras_list.append(key)

    return extras_list


def get_all():
    extras = ExtraModel.query.all()
    return jsonify(extras), 200


def get_specific_extra(extra_id):
    extras = ExtraModel.query.filter_by(id = extra_id).first()

    extras_list = filter_extras_true(extras)

    return {"msg": extras_list}, 200


# @jwt_required(locations=["headers"])
def create_extra(extras):
    new_extra = ExtraModel(extras)

    current_app.db.session.add(new_extra)
    current_app.db.session.commit()
 # chamar o true filter, e retonar
    return new_extra

def update_extra(extra_id):
    update_data = request.json
    
    updated_data = ExtraModel.query.filter_by(id = extra_id).update(update_data)

    current_app.db.session.commit()

    updated_data = ExtraModel.query.filter_by(id = extra_id).first()

    return jsonify(updated_data), 200

def delete_extra(extra_id):
    to_be_deleted = ExtraModel.query.filter_by(id = extra_id).first()

    current_app.db.session.delete(to_be_deleted)
    current_app.db.session.commit()

    return {}, 204