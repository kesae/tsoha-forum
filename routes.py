from flask import redirect, render_template, request
from app import app
import users


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/register", methods=["GET", "POST"])
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
        return render_template("error.html", message="Rekisteröinti ei onnistunut")
