import secrets


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_urlsafe(16)