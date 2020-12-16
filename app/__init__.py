from flask import Flask
from . import home, companies, company_page


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    app.register_blueprint(home.home)
    app.register_blueprint(companies.companies)
    app.register_blueprint(company_page.company_page)
    return app
