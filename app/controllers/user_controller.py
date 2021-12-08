from flask import jsonify, request, current_app
from app.models.user_model import UserModel
from app.controllers.address_controller import create_address

def create_user():
    data = request.get_json()

    data_address = data.pop("address")
   
    
    data['address_id'] = create_address(data_address)
    print(data)

    user = UserModel(**data)
    current_app.db.session.add(user)
    current_app.db.session.commit()
    
    return jsonify(user), 201




def update_user():
        ...


# discutir necessidade
def get_user():
        ...


# discutir necessidade
def delete_user():
        ...
