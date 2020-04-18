from os.path import abspath, dirname, join as joinpath
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

# Read the configuration file
PARENT_FOLDER = abspath(joinpath(dirname(__file__), ".."))
with open(joinpath(PARENT_FOLDER, ".config.json"), "r") as fp:
    config = json.load(fp)
# Instantiate the app
app = Flask(__name__)
# Set app configuration
for key, value in config.items():
    app.config[key] = value
# Database
db = SQLAlchemy(app)
# bcrypt for hashing and verifying passwords
bcrypt = Bcrypt()
# Login manager
login_manager = LoginManager(app)
login_manager.login_view = "user.login"
login_manager.login_message_category = "info"
# Mail
mail = Mail(app)

from flaskblog.users.routes import users # pylint: disable=wrong-import-position
from flaskblog.posts.routes import posts # pylint: disable=wrong-import-position
from flaskblog.main.routes import main # pylint: disable=wrong-import-position
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
