# pylint: disable=import-outside-toplevel
from os.path import abspath, dirname, join as joinpath
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

# Database
db = SQLAlchemy()
# bcrypt for hashing and verifying passwords
bcrypt = Bcrypt()
# Login manager
login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.login_message_category = "info"
# Mail
mail = Mail()


def create_app(config=Config):
    app = Flask(__name__)
    # Set the app configuration
    app.config.from_object(config)
    # Set the extensions configurations
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    # Register blueprints
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app
