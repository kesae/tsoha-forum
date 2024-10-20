from flask import redirect, url_for, g, Blueprint, session
import memberships
import errorpages


bp = Blueprint("membership", __name__)


@bp.before_request
def check_access():
    if not (g.user and g.user.is_admin):
        return errorpages.get_no_admin()


@bp.route("/group/<int:group_id>/join/<int:user_id>", methods=["POST"])
def add(group_id, user_id):
    memberships.add_membership(group_id, user_id)
    return redirect(url_for("user.show", user_id=user_id))


@bp.route("/group/<int:group_id>/remove/<int:user_id>", methods=["POST"])
def remove(group_id, user_id):
    memberships.remove_membership(group_id, user_id)
    if "url" in session:
        return redirect(session["url"])
    return redirect(url_for("group.show", group_id=group_id))
