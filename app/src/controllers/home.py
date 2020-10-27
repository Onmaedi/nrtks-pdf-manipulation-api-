from flask import jsonify, Blueprint, Flask

bp = Blueprint("home", __name__)

@bp.route("/")
def index():
    return jsonify({
        "message": "NRTKS API"
    })


def init_app(app: Flask):
    app.register_blueprint(bp)