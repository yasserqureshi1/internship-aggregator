from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def scrape_company_sites():
    print('Starting scrape')
    from app.webscraper import Scraper
    Scraper()
    print("Scrape done")


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)
    db.init_app(app)

    from . import home, companies, company_page
    app.register_blueprint(home.home)
    app.register_blueprint(companies.companies)
    app.register_blueprint(company_page.company_page)

    with app.app_context():
        db.create_all()
    app.app_context().push()

    sched = BackgroundScheduler(daemon=True)
    sched.add_job(scrape_company_sites, 'interval', hours=6)
    sched.start()

    return app