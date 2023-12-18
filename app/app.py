from flask import Flask
from app.configuration.configuration import Configuration


def init_config():
    app = Flask(__name__)
    Configuration(app).init_app()

    return app






