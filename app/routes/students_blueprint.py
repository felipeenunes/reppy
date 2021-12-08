from flask import Blueprint
from app.controllers.user_controller import create_user
bp = Blueprint("bp_student", __name__, url_prefix='/student')

bp.post("")(create_user)
bp.get("")
bp.patch("")
bp.delete("")

