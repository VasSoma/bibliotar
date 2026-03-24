from flask import Flask
from config import Config
from .extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    from flask_migrate import Migrate
    migrate = Migrate(app,db)

    from .main import bp
    app.register_blueprint(bp)

    return app