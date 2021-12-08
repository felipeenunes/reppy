from flask import request, current_app
from flask.json import jsonify
from werkzeug.exceptions import NotFound
from app.models.user_model import UserModel
def create_user():
        ...


def update_user():
        ...


def get_user_by_id(id):
        try:
                
                query = UserModel.query.filter_by(id=id).first_or_404()
                return jsonify(query),200

        except NotFound:
                return {"msg": "User not Found"},404

# discutir necessidade
def get_user():
        ...


# discutir necessidade
def delete_user(id):
        try:
                query = UserModel.filter_by(id=id).first_or_404()
                current_app.db.session.delete(query)
                current_app.db.session.commit()
                return '', 204
        except NotFound:
                return {"msg": "User not Found"},404

