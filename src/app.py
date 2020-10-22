from flask import Flask
from dotenv import load_dotenv
from dynaconf import FlaskDynaconf


def minimal_app():
    load_dotenv()
    app = Flask(__name__)
    return app


def create_app(**config):
    print(config)
    app = minimal_app()
    FlaskDynaconf(app)
    app.config.load_extensions()
    return app


