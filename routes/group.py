from flask import redirect, render_template, request, url_for, g, Blueprint
import groups
import memberships
import errorpages
from utils import check_password, create_page_numbers

bp = Blueprint("group", __name__)


@bp.before_request
def check_access():
    if not (g.user and g.user.is_admin):
        return errorpages.get_no_admin()


@bp.route("/groups")
def show_all():
    return render_template("groups.html", groups=groups.get_groups())


@bp.route("/group/<int:group_id>", methods=["GET", "POST"])
def show(group_id):
    PAGE_SIZE = 20
    try:
        member_page = int(request.args.get("mpage", 1))
    except ValueError:
        return errorpages.get_page_missing()
    group = groups.get_group(group_id)
    if not group:
        return errorpages.get_page_missing()
    member_count = memberships.get_group_member_count(group_id)
    last_page = max(0, member_count - 1) // (PAGE_SIZE) + 1
    limited_page = min(max(1, member_page), last_page)
    if limited_page != member_page:
        return redirect(
            url_for("group.show", group_id=group_id, mpage=limited_page)
        )
    page_numbers = create_page_numbers(member_page, last_page)
    members = memberships.get_paginated_members(group_id, member_page)
    return render_template(
        "group.html", group=group, members=members, page_numbers=page_numbers
    )


@bp.route("/group/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add-group.html")
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        if not 5 <= len(title) <= 30:
            return errorpages.get_title_length()
        if not len(description) <= 100:
            return errorpages.get_long_description()
        groups.add_group(title, description)
        return redirect(url_for("group.show_all"))


@bp.route("/group/<int:group_id>/edit", methods=["GET", "POST"])
def edit(group_id):
    group = groups.get_group(group_id)
    if not group:
        return errorpages.get_page_missing()
    if request.method == "GET":
        return render_template("edit-group.html", group=group)
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        if not 5 <= len(title) <= 30:
            return errorpages.get_title_length()
        if not len(description) <= 100:
            return errorpages.get_long_description()
        if groups.edit_group(group_id, title, description):
            return redirect(url_for("group.show_all"))
        return errorpages.get_reserved_group()


@bp.route("/group/<int:group_id>/remove", methods=["GET", "POST"])
def remove(group_id):
    group = groups.get_group(group_id)
    if not group:
        return errorpages.get_page_missing()
    if request.method == "GET":
        return render_template("remove-group.html", group=group)
    if request.method == "POST":
        password = request.form["password"]
        if not check_password(g.user.id, password):
            return errorpages.get_wrong_password()
        groups.remove_group(group_id)
        return redirect(url_for("group.show_all"))
