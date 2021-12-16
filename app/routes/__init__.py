from flask import Flask


def init_app(app: Flask) -> None:
    from .user_blueprint import bp as bp_user
    from .republics_blueprint import bp as bp_republics
    from.login_blueprint import bp as bp_login
    from .pictures_blueprint import bp as bp_pictures
    from .send_email_blueprint import bp as bp_email

    app.register_blueprint(bp_user)
    app.register_blueprint(bp_republics)
    app.register_blueprint(bp_login)
    app.register_blueprint(bp_pictures)
    app.register_blueprint(bp_email)
