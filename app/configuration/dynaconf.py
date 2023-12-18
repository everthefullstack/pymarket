from dynaconf import FlaskDynaconf
from flask import Flask


class Dynaconf:

    __slots__ = ("app",)

    def __init__(self, app:Flask) -> None:
        self.app = app

    def init_app(self):
        FlaskDynaconf(self.app)

def init_app(app: Flask):
    Dynaconf(app).init_app()