from app.blueprints.api.cnpj.repository import CnpjRepository
from app.utils.http_response import HttpResponse


class CnpjService():

    __slots__ = ("repository", "http_response")

    def __init__(self, repository: CnpjRepository, http_response: HttpResponse) -> None:
        self.repository = repository
        self.http_response = http_response

    def get_cnpjs(self, dataset):

        sql_where = ""
        len_codigos = len(dataset['cnpjs'])

        for x in range(0, len_codigos):
            sql_where += f"""(t1.cnpj_basico = '{dataset['cnpjs'][x][0:8]}' and 
                              t1.cnpj_ordem = '{dataset['cnpjs'][x][8:12]}' and 
                              t1.cnpj_dv = '{dataset['cnpjs'][x][12:14]}')"""
            
            if x < (len_codigos-1):
                sql_where += " or "
        
        res = self.repository.get_cnpjs(sql_where)

        if not isinstance(res, Exception):
            return self.http_response("msg", res, 200).http_response()
        
        else:
            return self.http_response("msg", f"error -> {res}", 500).http_response()


    