from apiflask import APIFlask
from flask_migrate import Migrate

from .config import Config
from .extensions import db
from flask_cors import CORS

def create_app(config_class=Config):
    app = APIFlask(__name__,json_errors=True,title="Bibliotar_API",docs_path="/swagger") #generate apiflask obj

    # Add CORS to avoid running both the backend and frontend on the same port
    CORS(app, origins=["http://localhost:5173"])

    app.config.from_object(config_class) # setup flask with config.py

    # Initialize db
    db.init_app(app)
    migrate = Migrate(app,db)

    from .blueprint import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/api')

    return app