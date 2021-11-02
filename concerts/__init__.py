from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login.login_manager import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)


def create_app():
    app.secret_key = "secret_key"

    # Setup bootstrap for quick forms
    bootstrap = Bootstrap(app)

    # Configure upload folder
    UPLOAD_FOLDER = "/concerts/static/images"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    # Setup sql alchemy
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgres://minovrqrwtozfg:66a1918e869dce9d35263b373131a3cb2ed8c7c98f3f9b2ccee1a451d5fad94a@ec2-3-217-91-165.compute-1.amazonaws.com:5432/d2od900bb0gmgn"
    db.init_app(app)

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.account"
    login_manager.login_message = "Please log in to access this feature."
    login_manager.init_app(app)

    # Error handling
    @app.errorhandler(404)
    def not_found(e):
        return render_template("pages/404.jinja"), 404

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template("pages/500.jinja"), 500

    # User loader function
    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Add blueprints
    from . import views, findevents, myevents, bookedevents, auth

    app.register_blueprint(views.mainbp)
    app.register_blueprint(findevents.bp)
    app.register_blueprint(myevents.bp)
    app.register_blueprint(bookedevents.bp)
    app.register_blueprint(auth.bp)
    return app
