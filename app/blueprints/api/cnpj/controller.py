from app.blueprints.api.cnpj.service import CnpjService
from flask import request


class CnpjController:

    __slots__ = ("service")

    def __init__(self, service: CnpjService) -> None:
        self.service = service

    def get_cnpjs(self):

        dataset = request.get_json()
        return self.service.get_cnpjs(dataset)
    



   


