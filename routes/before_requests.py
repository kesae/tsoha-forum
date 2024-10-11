from flask import request, session, abort, g, Blueprint
import users
from utils import check_csrf_token


bp = Blueprint("before_requests", __name__)


@bp.before_app_request
def load_session():
    g.user = None
    if "user_id" in session:
        g.user = users.get_user(session["user_id"])


@bp.before_app_request
def test_csrf_token():
    if "user_id" not in session:
        return
    if request.method == "POST":
        if not check_csrf_token():
            abort(403)
