from flask import Blueprint
from app.controllers.user_controller import login_user

bp = Blueprint("bp_login", __name__, url_prefix='/login')
bp.post("")(login_user)
