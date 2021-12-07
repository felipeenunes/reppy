from flask import Blueprint

bp = Blueprint("bp_republics", __name__, url_prefix='/republic')

bp.post("")
bp.get("")
bp.patch("")
bp.delete("")



