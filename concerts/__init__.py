from flask import Flask


def create_app():
    app = Flask(__name__)
    app.secret_key = "secret_key"

    from . import views

    app.register_blueprint(views.mainbp)
    return app
