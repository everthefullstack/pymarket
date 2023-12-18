from app.blueprints.api.dashboard.repository import DashboardRepository
from app.utils.http_response import HttpResponse


class DashboardService():

    __slots__ = ("repository", "http_response")

    def __init__(self, repository: DashboardRepository, http_response: HttpResponse) -> None:
        self.repository = repository
        self.http_response = http_response
    
    def get_dash_porte_set(self, dataset):

        res = self.repository.get_dash_porte_set(dataset)
        
        if not isinstance(res, Exception):
            return self.http_response("msg", res, 200).http_response()
        
        else:
            return self.http_response("msg", f"error -> {res}", 500).http_response()
    
    def get_dash_cresc_dec_set(self, dataset):

        res = self.repository.get_dash_cresc_dec_set(dataset)
            
        if not isinstance(res, Exception):
            return self.http_response("msg", res, 200).http_response()
        
        else:
            return self.http_response("msg", f"error -> {res}", 500).http_response()
        
    def get_periodo_setores(self):
        
        res = self.repository.get_periodo_setores()
            
        if not isinstance(res, Exception):
            return self.http_response("msg", res, 200).http_response()
        
        else:
            return self.http_response("msg", f"error -> {res}", 500).http_response()
        
    def get_periodo_portes(self):
        
        res = self.repository.get_periodo_portes()
            
        if not isinstance(res, Exception):
            return self.http_response("msg", res, 200).http_response()
        
        else:
            return self.http_response("msg", f"error -> {res}", 500).http_response()