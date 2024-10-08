from flask import render_template


def get_login_error():
    message = "Toiminto vaatii kirjautumisen"
    return render_template("error.html", message=message), 403


def get_access_error():
    message = "Pääsy estetty"
    return render_template("error.html", message=message), 403


def get_admin_error():
    message = "Toiminto vaatii kirjautumisen järjestelmänvalvojana"
    return render_template("error.html", message=message)


def get_missing_error():
    message = "Sivua ei löydy"
    return render_template("error.html", message=message), 404


def get_password_error():
    message = "Väärä salasana"
    return render_template("error.html", message=message), 401


def get_reserved_username_error():
    message = "Käyttäjänimi on jo varattu"
    return render_template("error.html", message=message), 409
