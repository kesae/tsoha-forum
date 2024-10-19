import secrets
from flask import request, session, g
from werkzeug.security import check_password_hash
from boards import nonadmin_has_access, get_user_boards
import users


def set_csrf_token():
    session["csrf_token"] = secrets.token_hex(16)


def check_csrf_token():
    if "csrf_token" not in request.form:
        return False
    return session["csrf_token"] == request.form["csrf_token"]


def check_board_access(board_id):
    if g.user and g.user.is_admin:
        return True
    user_id = session.get("user_id", 0)
    return nonadmin_has_access(user_id, board_id)


def get_boards():
    user_id = session.get("user_id", 0)
    return get_user_boards(user_id)


def check_password(user_id, password):
    pw_hash = users.get_password_hash(user_id).password
    if not pw_hash:
        return False
    return check_password_hash(pw_hash, password)


def create_page_numbers(page, last_page):
    result = set()
    result.add(1)
    result.add(page)
    result.add(last_page)
    for n in range(0, 10):
        prev = int(round(page - 10**n + 0.1, -n))
        prev2 = prev + 10**n // 2
        result.add(prev)
        result.add(prev2)
        nxt = int(round(page + 10**n - 0.1, -n))
        nxt2 = nxt - 10**n // 2
        result.add(nxt)
        result.add(nxt2)
    result = list(filter(lambda x: 1 <= x <= last_page, list(result)))
    result.sort()
    return result
