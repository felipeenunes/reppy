from flask import Flask
from flask_migrate import Migrate


def init_app(app: Flask):
    from app.models.address_model import AddressModel
    from app.models.user_model import UserModel
    from app.models.republic_model import RepublicModel
    from app.models.picture_model import PictureModel
    from app.models.extras_model import ExtraModel

    Migrate(app, app.db)
