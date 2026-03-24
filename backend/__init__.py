from flask import Flask
from config import Config
from .extensions import db

def create_app(config_class=Config): #got a config.py
    app = Flask(__name__) #gen flask obj
    app.config.from_object(config_class) # setup flask with config.py

    db.init_app(app) # flask + database connection

    from flask_migrate import Migrate
    migrate = Migrate(app,db) # helper, modify database if smt changed

    from .main import bp
    app.register_blueprint(bp) # regist blueprint with bp

    return app