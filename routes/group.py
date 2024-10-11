from flask import redirect, render_template, request, url_for, g, Blueprint
import groups
import pages


bp = Blueprint("group", __name__)


@bp.route("/groups")
def show_all():
    if not (g.user and g.user.is_admin):
        return pages.get_admin_error()
    return render_template("groups.html", groups=groups.get_groups())


@bp.route("/group/<int:group_id>", methods=["GET", "POST"])
def show(group_id):
    if not (g.user and g.user.is_admin):
        return pages.get_admin_error()
    group = groups.get_group(group_id)
    if not group:
        return pages.get_missing_error()
    return render_template("group.html", group=group)


@bp.route("/group/add", methods=["GET", "POST"])
def add():
    if not (g.user and g.user.is_admin):
        return pages.get_admin_error()
    if request.method == "GET":
        return render_template("add-group.html")
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        groups.add_group(title, description)
        return redirect(url_for("group.show_all"))
