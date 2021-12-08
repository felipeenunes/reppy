from flask import Blueprint

from app.controllers.republics_controller import create_republic, get_all_republics

bp = Blueprint("bp_republics", __name__, url_prefix='/republic')

bp.post("")(create_republic)
bp.get("")(get_all_republics)
bp.patch("")
bp.delete("")



