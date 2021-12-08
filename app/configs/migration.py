from flask import Flask
from flask_migrate import Migrate


def init_app(app: Flask):
    from app.models.adress_model import AdressModel
    from app.models.picture_model import PictureModel
    from app.models.republic_model import RepublicModel
    from app.models.state_model import StateModel
    from app.models.user_model import UserModel


    Migrate(app, app.db)
