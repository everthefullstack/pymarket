from app.blueprints.api.cnae.repository import CnaeRepository
from app.utils.http_response import HttpResponse


class CnaeService():

    __slots__ = ("repository", "http_response")

    def __init__(self, repository: CnaeRepository, http_response: HttpResponse) -> None:
        self.repository = repository
        self.http_response = http_response

    def get_cnaes(self, dataset):
        
        res = None
        sql_where = ""

        if dataset["ufs"]:
            sql_where += (f"t2.uf in {str(tuple(dataset['ufs']))}" if len(dataset['ufs']) > 1 
                            else
                            f"t2.uf in {str(tuple(dataset['ufs'])).replace(',', '')}")
            
        if dataset["municipios"]:
            sql_where += (f" and t2.municipio in {str(tuple(dataset['municipios']))}" if len(dataset['municipios']) > 1 
                            else
                            f" and t2.municipio in {str(tuple(dataset['municipios'])).replace(',', '')}")

        if dataset["tipo"] == "p":
            sql_where += (f" and t2.cnae_primario in {str(tuple(dataset['codigos']))}" if len(dataset['codigos']) > 1 
                         else 
                         f" and t2.cnae_primario in {str(tuple(dataset['codigos'])).replace(',', '')}")

            res = self.repository.get_cnaes(sql_where)
        
        elif dataset["tipo"] == "s":

            sql_where += " and t2.cnae_secundario like "
            len_codigos = len(dataset['codigos'])

            for x in range(0, len_codigos):
                sql_where += f"'%%{dataset['codigos'][x]}%%'"
                
                if x < (len_codigos-1):
                    sql_where += " or t2.cnae_secundario like "

            res = self.repository.get_cnaes(sql_where)

        if not isinstance(res, Exception):
            return self.http_response("msg", res, 200).http_response()
        
        else:
            return self.http_response("msg", f"error -> {res}", 500).http_response()
    