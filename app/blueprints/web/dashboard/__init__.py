from flask import Flask, Blueprint
from app.blueprints.web.dashboard.view import dashboard


def init_app(app: Flask):
    
    bp = Blueprint("dashboard_web", __name__, url_prefix="/dashboard", template_folder="templates", static_folder="static")
    bp.add_url_rule(rule="", view_func=dashboard, methods=["GET"])

    app.register_blueprint(bp)