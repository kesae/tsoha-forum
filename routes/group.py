from flask import redirect, render_template, request, url_for, g, Blueprint
import groups
import pages
from utils import check_password

bp = Blueprint("group", __name__)


@bp.before_request
def check_access():
    if not (g.user and g.user.is_admin):
        return pages.get_admin_error()


@bp.route("/groups")
def show_all():
    return render_template("groups.html", groups=groups.get_groups())


@bp.route("/group/<int:group_id>", methods=["GET", "POST"])
def show(group_id):
    group = groups.get_group(group_id)
    if not group:
        return pages.get_missing_error()
    return render_template("group.html", group=group)


@bp.route("/group/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add-group.html")
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        if not 5 <= len(title) <= 30:
            return pages.get_title_length_error()
        if not len(description) <= 100:
            return pages.get_long_description_error()
        groups.add_group(title, description)
        return redirect(url_for("group.show_all"))


@bp.route("/group/<int:group_id>/edit", methods=["GET", "POST"])
def edit(group_id):
    group = groups.get_group(group_id)
    if not group:
        return pages.get_missing_error()
    if request.method == "GET":
        return render_template("edit-group.html", group=group)
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        if not 5 <= len(title) <= 30:
            return pages.get_title_length_error()
        if not len(description) <= 100:
            return pages.get_long_description_error()
        if groups.edit_group(group_id, title, description):
            return redirect(url_for("group.show_all"))
        return pages.get_reserved_group_error()


@bp.route("/group/<int:group_id>/remove", methods=["GET", "POST"])
def remove(group_id):
    group = groups.get_group(group_id)
    if not group:
        return pages.get_missing_error()
    if request.method == "GET":
        return render_template("remove-group.html", group=group)
    if request.method == "POST":
        password = request.form["password"]
        if not check_password(g.user.id, password):
            return pages.get_password_error()
        groups.remove_group(group_id)
        return redirect(url_for("group.show_all"))
