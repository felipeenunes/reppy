from flask import jsonify, request, current_app
from app.models.adress_model import AdressModel
from app.models.user_model import UserModel
from app.models.state_model import StateModel

def create_user():
    data = request.get_json()
    data_adress = {key:value for key,value in data.items() if key == "adress"}
    del data['adress']
   # data['address_id'] = 
    user = UserModel(**data)
    current_app.db.session.add(user)
    current_app.db.session.commit()




def update_user():
        ...


# discutir necessidade
def get_user():
        ...


# discutir necessidade
def delete_user():
        ...
