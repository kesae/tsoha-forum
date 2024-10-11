from flask import render_template, Blueprint
from utils import get_boards


bp = Blueprint("index", __name__)


@bp.route("/")
def show():
    return render_template("index.html", boards=get_boards())
