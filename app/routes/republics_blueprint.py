from flask import Blueprint

from app.controllers.republics_controller import create_republic, delete_republic, get_all_republics, get_one, update_republic

bp = Blueprint("bp_republics", __name__, url_prefix='/republic')

bp.post("")(create_republic)
bp.get("")(get_all_republics)
bp.get("/<int:id>")(get_one)
bp.patch("/<int:id>")(update_republic)
bp.delete("/<int:id>")(delete_republic)



