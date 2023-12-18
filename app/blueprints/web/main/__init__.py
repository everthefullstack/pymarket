from flask import Flask, Blueprint


def init_app(app: Flask):
    
    bp = Blueprint("main_web", __name__, url_prefix="/main", static_folder="static", template_folder="templates")
    app.register_blueprint(bp)