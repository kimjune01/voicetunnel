import os
import sys

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

current_path = os.getcwd()
sys.path.insert(0, current_path + '/../')
from src.config import app_config

# db init

db = SQLAlchemy()
config_name = os.environ['FLASK_CONFIG']
config = app_config[config_name]

def create_app(config_name):
    app = Flask(__name__, template_folder="webpages/templates")
    app.config.from_object(app_config[config_name])
    app.secret_key = "s3cr3t"  # need for flask for some reason

    SQLALCHEMY_DATABASE_URI = os.environ['development_db']
    if config_name =="production":
        SQLALCHEMY_DATABASE_URI = os.environ['production_db']
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    
    Bootstrap(app)
    db.init_app(app)

    migrate = Migrate(app,db)

    # database models

    # this is how you register your database model as part of the crud to an application endpoint
    #####################
    #### blueprints #####
    #####################
    return app