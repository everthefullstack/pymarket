from flask import Flask, Blueprint
from app.blueprints.api.dashboard.service import DashboardService
from app.blueprints.api.dashboard.controller import DashboardController
from app.blueprints.api.dashboard.repository import DashboardRepository
from app.utils.http_response import HttpResponse


def init_app(app: Flask):
    
    http_response = HttpResponse
    repository = DashboardRepository()
    service = DashboardService(repository, http_response)
    controller = DashboardController(service)

    bp = Blueprint("dashboard", __name__, url_prefix="/api/v1/dashboard")
    bp.add_url_rule(rule="/get_dash_cresc_dec_set", view_func=controller.get_dash_cresc_dec_set, methods=["POST"]) #crescimento e declínio dos setores
    bp.add_url_rule(rule="/get_dash_porte_set", view_func=controller.get_dash_porte_set, methods=["POST"]) #porte de cada setor
    bp.add_url_rule(rule="/get_periodo_setores", view_func=controller.get_periodo_setores, methods=["GET"])
    bp.add_url_rule(rule="/get_periodo_portes", view_func=controller.get_periodo_portes, methods=["GET"])

    app.register_blueprint(bp)