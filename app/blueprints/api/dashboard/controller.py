from app.blueprints.api.dashboard.service import DashboardService
from flask import request

class DashboardController:

    __slots__ = ("service")

    def __init__(self, service: DashboardService) -> None:
        self.service = service

    def get_dash_cresc_dec_set(self):
        dataset = request.get_json()
        return self.service.get_dash_cresc_dec_set(dataset)
    
    def get_dash_porte_set(self):
        dataset = request.get_json()
        return self.service.get_dash_porte_set(dataset)
   
    def get_periodo_setores(self):
        return self.service.get_periodo_setores()
    
    def get_periodo_portes(self):
        return self.service.get_periodo_portes()



   


