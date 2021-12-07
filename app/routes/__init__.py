from flask import Flask


def init_app(app: Flask) -> None:
    from .students_blueprint import bp as bp_students
    from .republics_blueprint import bp as bp_republics

    app.register_blueprint(bp_students)
    app.register_blueprint(bp_republics)
