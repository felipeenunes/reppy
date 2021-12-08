from flask import request, current_app, jsonify
from werkzeug.exceptions import NotFound
from app.models.user_model import UserModel
from app.controllers.address_controller import create_address

def create_user():
    data = request.get_json()

    data_address = data.pop("address")
    
    data['address_id'] = create_address(data_address)

    user = UserModel(**data)
    current_app.db.session.add(user)
    current_app.db.session.commit()
    
    return jsonify(user), 201




def update_user():
        ...


def get_user_by_id(cpf):
        try:
                
                query = UserModel.query.filter_by(cpf=cpf).first_or_404()
                return jsonify(query),200

        except NotFound:
                return {"msg": "User not Found"},404

# discutir necessidade
def delete_user(cpf):
        try:
                query = UserModel.query.filter_by(cpf=cpf).first_or_404()
                current_app.db.session.delete(query)
                current_app.db.session.commit()
                return '', 204
        except NotFound:
                return {"msg": "User not Found"},404

