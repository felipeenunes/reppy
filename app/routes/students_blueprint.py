from flask import Blueprint

bp = Blueprint("bp_student", __name__, url_prefix='/student')

bp.post("")
bp.get("")
bp.patch("")
bp.delete("")

