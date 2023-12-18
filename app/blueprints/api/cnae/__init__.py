from flask import Flask, Blueprint
from app.blueprints.api.cnae.service import CnaeService
from app.blueprints.api.cnae.controller import CnaeController
from app.blueprints.api.cnae.repository import CnaeRepository
from app.utils.http_response import HttpResponse


def init_app(app: Flask):
    
    http_response = HttpResponse
    repository = CnaeRepository()
    service = CnaeService(repository, http_response)
    controller = CnaeController(service)

    bp = Blueprint("cnae", __name__, url_prefix="/api/v1/cnae")
    bp.add_url_rule(rule="/get_cnaes", view_func=controller.get_cnaes, methods=["GET"]) 

    app.register_blueprint(bp)

    