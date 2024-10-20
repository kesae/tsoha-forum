from flask import (
    session,
    redirect,
    render_template,
    request,
    url_for,
    g,
    Blueprint,
)
import users
import groups
from utils import check_password, create_page_numbers
import errorpages


bp = Blueprint("user", __name__)


@bp.route("/users")
def show_all():
    page_size = 20
    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        return errorpages.get_page_missing()
    user_count = users.get_user_count()
    last_page = max(0, user_count - 1) // (page_size) + 1
    limited_page = min(max(1, page), last_page)
    if limited_page != page:
        return redirect(url_for("page.show_all", page=limited_page))
    page_numbers = create_page_numbers(page, last_page)
    return render_template(
        "users.html",
        users=users.get_paginated_users(page=page),
        page_numbers=page_numbers,
    )


@bp.route("/user/<int:user_id>")
def show(user_id):
    user = users.get_user(user_id)
    user_groups = groups.get_user_groups(user_id)
    joinable_groups = groups.get_joinable_groups(user_id)
    return render_template(
        "user.html",
        user=user,
        groups=user_groups,
        joinable_groups=joinable_groups,
    )


@bp.route("/user/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if 2 <= len(username) <= 30:
            return errorpages.get_username_length()
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if len(password1) < 10:
            errorpages.get_short_password()
        if users.register(username, password1):
            return redirect(url_for("index.show"))
        return errorpages.get_reserved_username()


@bp.route("/user/<int:user_id>/remove", methods=["GET", "POST"])
def remove(user_id):
    if not g.user:
        return errorpages.get_no_login()
    if not (g.user.id == user_id or g.user.is_admin):
        return errorpages.get_no_access()
    if request.method == "GET":
        user = users.get_user(user_id)
        if not user:
            return errorpages.get_page_missing()
        return render_template("remove-user.html", user=user)
    if request.method == "POST":
        password = request.form["password"]
        if not check_password(g.user.id, password):
            return errorpages.get_wrong_password()
        users.remove_user(user_id)
        if user_id == g.user.id:
            del session["user_id"]
            return redirect(url_for("index.show"))
        return redirect(url_for("user.show_all"))
