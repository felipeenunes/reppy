from flask import Blueprint
from app.controllers.email_controller import send_email
bp = Blueprint("bp_email", __name__, url_prefix='/send-email')

bp.post("")(send_email)