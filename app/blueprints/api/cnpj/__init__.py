from flask import Flask, Blueprint
from app.blueprints.api.cnpj.service import CnpjService
from app.blueprints.api.cnpj.controller import CnpjController
from app.blueprints.api.cnpj.repository import CnpjRepository
from app.utils.http_response import HttpResponse


def init_app(app: Flask):
    
    http_response = HttpResponse
    repository = CnpjRepository()
    service = CnpjService(repository, http_response)
    controller = CnpjController(service)

    bp = Blueprint("cnpj", __name__, url_prefix="/api/v1/cnpj")
    bp.add_url_rule(rule="/get_cnpjs", view_func=controller.get_cnpjs, methods=["GET"]) 

    app.register_blueprint(bp)