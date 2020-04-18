from os.path import abspath, dirname, join as joinpath
import json

PARENT_FOLDER = abspath(joinpath(dirname(__file__), ".."))
CONFIG_FILEPATH = joinpath(PARENT_FOLDER, ".config.json")

with open(CONFIG_FILEPATH, "r") as fp:
    config = json.load(fp)


class Config(object):
    SECRET_KEY = config.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = config.get("SQLALCHEMY_DATABASE_URI")
    MAIL_SERVER = config.get("MAIL_SERVER")
    MAIL_PORT = config.get("MAIL_PORT")
    MAIL_USERNAME = config.get("MAIL_USERNAME")
    MAIL_PASSWORD = config.get("MAIL_PASSWORD")
    MAIL_USE_TLS = config.get("MAIL_USE_TLS")
    MAIL_USE_SSL = config.get("MAIL_USE_SSL")
