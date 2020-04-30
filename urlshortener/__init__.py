from flask import Flask
from urlshortener.database import db
from config import config


def create_app(config_name):
    app = Flask(__name__)  # instance_relative_config=True
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    print(f"APP RUNNING IN {config_name} MODE")
    db.init_app(app)
    #from .api import api_blueprint
    #app.register_blueprint(api_blueprint, url_prefix='/api')
    # routes & custom errors here

    @app.route('/')
    def index():
        return "<h1>It works!</h1>"

    return app
