import secrets
from flask import request, session
from boards import user_has_access


def set_csrf_token():
    session["csrf_token"] = secrets.token_hex(16)


def check_csrf_token():
    if "csrf_token" not in request.form:
        return False
    return session["csrf_token"] == request.form["csrf_token"]


def check_board_access(board_id):
    user_id = session.get("user_id", 0)
    return user_has_access(user_id, board_id)
