from flask import Flask, Blueprint
from app.blueprints.web.index.view import index, index_redirect


def init_app(app: Flask):
    
    bp1 = Blueprint("index_redirect", __name__, url_prefix="/")
    bp1.add_url_rule(rule="", view_func=index_redirect, methods=["GET"])
    
    app.register_blueprint(bp1)

    bp2 = Blueprint("index_web", __name__, url_prefix="/index", template_folder="templates", static_folder="static")
    bp2.add_url_rule(rule="", view_func=index, methods=["GET"])
    
    app.register_blueprint(bp2)


    