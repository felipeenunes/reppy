from flask import Flask
from flask_migrate import Migrate


def init_app(app: Flask):
    from app.models.state_model import StateModel
    from app.models.adress_model import AdressModel
    from app.models.user_model import UserModel
    from app.models.republic_model import RepublicModel
    from app.models.picture_model import PictureModel


    Migrate(app, app.db)
