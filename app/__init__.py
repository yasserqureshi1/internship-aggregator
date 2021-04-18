from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()




def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)
    db.init_app(app)

    from . import views
    app.register_blueprint(views.views)

    with app.app_context():
        db.create_all()
        db.session.commit()
    app.app_context().push()

    db.session.commit()
    
    return app
