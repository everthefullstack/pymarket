from app.blueprints.api.cnae.service import CnaeService
from flask import request


class CnaeController:

    __slots__ = ("service")

    def __init__(self, service: CnaeService) -> None:
        self.service = service

    def get_cnaes(self):

        dataset = request.get_json()
        return self.service.get_cnaes(dataset)
    
    



   


