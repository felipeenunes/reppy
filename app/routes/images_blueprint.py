from flask import Blueprint
from app.controllers.images_controller import delete_picture_img, patch_picture_img
bp = Blueprint('images_bp', __name__, url_prefix='/republic/<int:republic_id>/images/<int:img_id>')


bp.delete("")(delete_picture_img)
bp.patch("")(patch_picture_img)

