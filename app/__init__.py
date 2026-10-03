from flask import Flask
from flask_login import LoginManager

from app.config import Config
from .models import db, User, Prediction


# ---------------------------------------------------------
# Login Manager
# ---------------------------------------------------------

login_manager = LoginManager()


def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    # -----------------------------------------------------
    # Configuration
    # -----------------------------------------------------

    app.config.from_object(Config)

    # -----------------------------------------------------
    # Database
    # -----------------------------------------------------

    db.init_app(app)

    # -----------------------------------------------------
    # Flask Login
    # -----------------------------------------------------

    login_manager.init_app(app)

    # Login route is directly defined in run.py
    login_manager.login_view = "login"

    login_manager.login_message = "Please login to continue."
    login_manager.login_message_category = "warning"

    # -----------------------------------------------------
    # User Loader
    # -----------------------------------------------------

    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(int(user_id))

    # -----------------------------------------------------
    # Create Database Tables
    # -----------------------------------------------------

    with app.app_context():

        db.create_all()

    return app