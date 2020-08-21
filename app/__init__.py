# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    Bootstrap(app)
    db.init_app(app)



    login_manager.init_app(app)
    login_manager.login_message = "Vous devez vous connecter pour acceder a cette page."
    login_manager.login_view = "auth_microservice.login"

    migrate = Migrate(app, db)

      

    from app import models
    

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth_microservice as auth_microservice_blueprint
    app.register_blueprint(auth_microservice_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

  
    return app
