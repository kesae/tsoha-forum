from flask import render_template


def get_no_login():
    message = "Toiminto vaatii kirjautumisen"
    return render_template("error.html", message=message), 403


def get_no_access():
    message = "Pääsy estetty"
    return render_template("error.html", message=message), 403


def get_no_admin():
    message = "Toiminto vaatii kirjautumisen järjestelmänvalvojana"
    return render_template("error.html", message=message)


def get_page_missing():
    message = "Sivua ei ole"
    return render_template("error.html", message=message), 404


def get_wrong_password():
    message = "Väärä salasana"
    return render_template("error.html", message=message), 401


def get_reserved_username():
    message = "Käyttäjänimi on jo varattu"
    return render_template("error.html", message=message), 409


def get_reserved_board():
    message = "Samanniminen alue on jo olemassa"
    return render_template("error.html", message=message), 409


def get_reserved_group():
    message = "Samanniminen käyttäjäryhmä on jo olemassa"
    return render_template("error.html", message=message), 409


def get_title_length():
    message = "Otsikossa tulee olla vähintään 5 ja enintään 10 merkkiä"
    return render_template("error.html", message=message), 400


def get_long_description():
    message = "Kuvauksessa tulee olla enintään 100 merkkiä"
    return render_template("error.html", message=message), 400


def get_post_length():
    message = (
        "Viestin pituuden tulee olla vähintään 5 ja enintään 10 000 merkkiä"
    )
    return render_template("error.html", message=message), 400


def get_username_length():
    message = (
        "Käyttäjätunnuksessa tulee olla vähintään 2 ja enintään 30 merkkiä"
    )
    return render_template("error.html", message=message), 400


def get_short_password():
    message = "Salasanassa tulee olla vähintään 10 merkkiä"
    return render_template("error.html", message=message), 400
