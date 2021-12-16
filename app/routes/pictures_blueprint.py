from flask import Blueprint
from app.controllers.pictures_controller import delete_picture, patch_picture
bp = Blueprint('pictures_bp', __name__, url_prefix='/republic/<int:republic_id>/picture/<int:img_id>')


bp.delete("")(delete_picture)
bp.patch("")(patch_picture)
