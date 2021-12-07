from flask import Flask
from app import routes
from dotenv import load_dotenv
from os import environ
from app.configs import database, migration


load_dotenv()

def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False


    database.init_app(app)
    migration.init_app(app)
    routes.init_app(app)

    return app