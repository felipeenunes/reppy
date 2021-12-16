from app.models.extras_model import ExtraModel
from flask import current_app
from flask_jwt_extended import jwt_required

def filter_extras_true(extras):
    print(extras)
    extras = extras.__dict__

    if 'id' in extras: del extras['id']

    extras_list = []
    for key, value in extras.items():
        print(key, value)
        if value and key != '_sa_instance_state' and key != 'republic_id':
            extras_list.append(key)
    return extras_list


def complete_extras_with_false(extras):
    extras_keys = ['animals_allowed', 'parties_allowed', 'wifi', 'swiming_pool','grill']

    for key in extras_keys:
        if key not in extras:
            extras[key] = False

    return extras

@jwt_required(locations=["headers"])
def create_extra(extras):
    extras = complete_extras_with_false(extras)

    new_extra = ExtraModel(**extras)

    new_extra_list = filter_extras_true(new_extra)
    current_app.db.session.add(new_extra)
    current_app.db.session.commit()

    return new_extra_list


@jwt_required(locations=["headers"])
def update_extra(update_data, updating_republic_id):
    update_data = complete_extras_with_false(update_data)

    updated_data = ExtraModel.query.filter_by(republic_id = updating_republic_id).update(update_data)

    current_app.db.session.commit()

    updated_data = ExtraModel.query.filter_by(republic_id = updating_republic_id).first()
    updated_data_list = filter_extras_true(updated_data)
    
    return updated_data_list
