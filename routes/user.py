from flask import redirect, render_template, request, url_for, g, Blueprint
import users
import groups
from utils import check_password
import pages


bp = Blueprint("user", __name__)


@bp.route("/users")
def show_all():
    return render_template("users.html", users=users.get_users())


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
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        return pages.get_reserved_username_error()


@bp.route("/user/<int:user_id>/remove", methods=["GET", "POST"])
def remove(user_id):
    if not g.user:
        return pages.get_login_error()
    if not (g.user.id == user_id or g.user.is_admin):
        return pages.get_access_error()
    if request.method == "GET":
        user = users.get_user(user_id)
        if not user:
            return pages.get_missing_error()
        return render_template("remove-user.html", user=user)
    if request.method == "POST":
        password = request.form["password"]
        if not check_password(g.user.id, password):
            return pages.get_password_error()
        users.remove_user(user_id)
        if user_id == g.user.id:
            return redirect(url_for("session.log_out"))
        return redirect(url_for("user.show_all"))
