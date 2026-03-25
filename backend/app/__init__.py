from apiflask import APIFlask
from .config import Config
from .extensions import db

def create_app(config_class=Config):
    app = APIFlask(__name__,json_errors=True,title="Bibliotar_API",docs_path="/swagger") #generate apiflask obj
    app.config.from_object(config_class) # setup flask with config.py

    db.init_app(app) # flask + database connection

    # from flask_migrate import Migrate
    # migrate = Migrate(app,db) # helper, modify database if smt changed

    from .blueprint import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/api')

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    return app