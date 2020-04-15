from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# Configuration
app.config["SECRET_KEY"] = "e537a8bc61e1b4aff62b664c42c2889a"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
# Database
db = SQLAlchemy(app)
# bcrypt for hashing and verifying passwords
bcrypt = Bcrypt()
# Login manager
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from flaskblog import routes
