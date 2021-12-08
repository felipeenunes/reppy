from flask import Flask


def init_app(app: Flask) -> None:
    from .user_blueprint import bp as bp_user
    from .republics_blueprint import bp as bp_republics

    app.register_blueprint(bp_user)
    app.register_blueprint(bp_republics)
