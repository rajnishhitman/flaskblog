from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# Configuration
app.config["SECRET_KEY"] = "e537a8bc61e1b4aff62b664c42c2889a"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

from flaskblog import routes

