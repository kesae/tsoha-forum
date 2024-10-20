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


def get_reserved_board_error():
    message = "Samanniminen alue on jo olemassa"
    return render_template("error.html", message=message), 409


def get_reserved_group_error():
    message = "Samanniminen käyttäjäryhmä on jo olemassa"
    return render_template("error.html", message=message), 409


def get_title_length_error():
    message = "Otsikossa tulee olla vähintään 5 ja enintään 10 merkkiä"
    return render_template("error.html", message=message), 400


def get_long_description_error():
    message = "Kuvauksessa tulee olla enintään 100 merkkiä"
    return render_template("error.html", message=message), 400


def get_post_length_error():
    message = (
        "Viestin pituuden tulee olla vähintään 5 ja enintään 10 000 merkkiä"
    )
    return render_template("error.html", message=message), 400


def get_username_length_error():
    message = (
        "Käyttäjätunnuksessa tulee olla vähintään 2 ja enintään 30 merkkiä"
    )
    return render_template("error.html", message=message), 400


def get_short_password_error():
    message = "Salasanassa tulee olla vähintään 10 merkkiä"
    return render_template("error.html", message=message), 400
