from flask import Flask


def init_app(app: Flask) -> None:
    from .user_blueprint import bp as bp_user
    from .republics_blueprint import bp as bp_republics
    from.login_blueprint import bp as bp_login
    from .images_blueprint import bp as bp_images
    from .send_email_blueprint import bp as bp_email
    from .extras_blueprint import bp as bp_extra

    app.register_blueprint(bp_user)
    app.register_blueprint(bp_republics)
    app.register_blueprint(bp_login)
    app.register_blueprint(bp_images)
    app.register_blueprint(bp_email)
    app.register_blueprint(bp_extra)
