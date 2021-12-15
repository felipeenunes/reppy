from flask import Blueprint
from app.controllers.extra_controller import get_all, create_extra, update_extra, get_specific_extra, delete_extra

bp = Blueprint("bp_extras", __name__, url_prefix="/extra")

bp.get("")(get_all)
bp.get("/<int:extra_id>")(get_specific_extra)
bp.post("")(create_extra)
bp.patch("/<int:extra_id>")(update_extra)
bp.delete("/<int:extra_id>")(delete_extra)