from flask import Blueprint, Flask
from flask_restful import Api
from .resources.merge import PdfMerger
from .resources.write import PdfWriter

bp = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(bp)


def init_app(app: Flask):
    api.add_resource(PdfMerger, "/pdf-merge")
    api.add_resource(PdfWriter, "/pdf-write")
    app.register_blueprint(bp)
