from flask import Flask
from importlib import import_module
import dynaconf


class Modules:

    __slots__ = ("app", "settings")

    def __init__(self, app:Flask) -> None:
        self.app = app
        self.settings = dynaconf.settings

    def __import_modules_list(self):
        for modules in self.settings["IMPORT_MODULES"]:
            for extension in self.settings[modules]:
                import_module(extension).init_app(self.app)
                print(f"Módulo {extension} configurado com sucesso.")

    def init_app(self):
        self.__import_modules_list()
