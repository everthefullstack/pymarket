from flask import Flask
from flask_cors import CORS


class Cors:

    __slots__ = ("app",)
    
    def __init__(self, app:Flask) -> None:
        self.app = app

    def init_app(self):
        CORS(self.app)

def init_app(app: Flask):
    Cors(app).init_app()