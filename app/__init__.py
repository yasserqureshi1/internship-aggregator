from flask import Flask
from . import home, companies


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    app.register_blueprint(home.home)
    app.register_blueprint(companies.companies)
    return app
