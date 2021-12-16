from flask import Blueprint
from app.controllers.user_controller import create_user, update_user, delete_user
bp = Blueprint("bp_user", __name__, url_prefix='/user')

bp.post("")(create_user)
bp.patch("")(update_user)
bp.delete("")(delete_user)
