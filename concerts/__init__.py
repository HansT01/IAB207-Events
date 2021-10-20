from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login.login_manager import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# CREATING DATABASE FILE
# from travel import db, create_app
# app = create_app()
# ctx = app.app_context()
# ctx.push()
# db.create_all()
# quit()


def create_app():
    app = Flask(__name__)
    app.secret_key = "secret_key"

    # Setup bootstrap for quick forms
    bootstrap = Bootstrap(app)

    # Configure upload folder
    UPLOAD_FOLDER = "/static/image"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    # Setup sql alchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.sqlite"
    db.init_app(app)

    # Add blueprints
    from . import views

    app.register_blueprint(views.mainbp)
    return app
