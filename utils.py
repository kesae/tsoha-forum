import secrets
from flask import request, session


def set_csrf_token():
    session["csrf_token"] = secrets.token_hex(16)


def check_csrf_token():
    if "csrf_token" not in request.form:
        return False
    return session["csrf_token"] == request.form["csrf_token"]
