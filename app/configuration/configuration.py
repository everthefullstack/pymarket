from app.configuration.modules import Modules
from app.configuration.database import Database
from app.configuration.tables import Tables
from flask import Flask


class Configuration:

    __slots__ = ("app",)

    def __init__(self, app:Flask) -> None:
        self.app = app

    def init_app(self):
        Modules(self.app).init_app() #precisa do app, pois usa o padrão factory conforme o flask pede
        Database().init_app()
        Tables().init_app()
