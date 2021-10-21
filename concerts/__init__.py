from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login.login_manager import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

# CREATING DATABASE FILE
# from concerts import db, create_app
# app = create_app()
# ctx = app.app_context()
# ctx.push()
# db.create_all()
# quit()


def create_app():
    app.secret_key = "secret_key"

    # Setup bootstrap for quick forms
    bootstrap = Bootstrap(app)

    # Configure upload folder
    UPLOAD_FOLDER = "/concerts/static/images"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    # Setup sql alchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.sqlite"
    db.init_app(app)

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.login_view = "main.account"
    login_manager.init_app(app)

    # User loader function
    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Add blueprints
    from . import views

    app.register_blueprint(views.mainbp)
    return app
