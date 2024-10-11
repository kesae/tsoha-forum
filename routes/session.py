from flask import render_template, request, redirect, Blueprint
import users


bp = Blueprint("session", __name__)


@bp.route("/login", methods=["GET", "POST"])
def log_in():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        message = "Väärä käyttäjätunnus tai salasana"
        return render_template("error.html", message=message)


@bp.route("/logout")
def log_out():
    users.logout()
    return redirect("/")
