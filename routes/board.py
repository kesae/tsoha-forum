from flask import (
    redirect,
    render_template,
    request,
    abort,
    url_for,
    g,
    Blueprint,
)
import boards
import topics
import groups
from utils import check_board_access, get_boards, check_password
import pages


bp = Blueprint("board", __name__)


@bp.route("/boards")
def show_all():
    if not (g.user and g.user.is_admin):
        return pages.get_admin_error()
    return render_template("boards.html", boards=get_boards())


@bp.route("/board/add", methods=["GET", "POST"])
def add():
    if not (g.user and g.user.is_admin):
        return pages.get_admin_error()
    if request.method == "GET":
        access_groups = groups.get_groups()
        return render_template("add-board.html", access_groups=access_groups)
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        access_string = request.form["access_group"]
        try:
            access_group = int(access_string)
        except ValueError:
            abort(403)
        access_group = None if access_group < 1 else access_group
        if boards.add_board(title, description, access_group):
            return redirect(url_for("board.show_all"))
        return pages.get_reserved_board_error()


@bp.route("/board/<int:board_id>")
def show(board_id):
    if not check_board_access(board_id):
        return pages.get_access_error()
    board = boards.get_board(board_id)
    if not board:
        return pages.get_missing_error()
    board_topics = topics.get_topics(board_id)
    return render_template("board.html", board=board, topics=board_topics)


@bp.route("/board/<int:board_id>/edit", methods=["GET", "POST"])
def edit(board_id):
    if not (g.user and g.user.is_admin):
        return pages.get_admin_error()
    board = boards.get_board(board_id)
    if not board:
        return pages.get_missing_error()
    if request.method == "GET":
        access_groups = groups.get_groups()
        return render_template(
            "edit-board.html", board=board, access_groups=access_groups
        )
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        access_string = request.form["access_group"]
        try:
            access_group = int(access_string)
        except ValueError:
            abort(403)
        access_group = None if access_group < 1 else access_group
        if boards.edit_board(board_id, title, description, access_group):
            return redirect(url_for("board.show_all"))
        return pages.get_reserved_board_error()


@bp.route("/board/<int:board_id>/remove", methods=["GET", "POST"])
def remove(board_id):
    if not (g.user and g.user.is_admin):
        return pages.get_admin_error()
    board = boards.get_board(board_id)
    if not board:
        return pages.get_missing_error()
    if request.method == "GET":
        return render_template("remove-board.html", board=board)
    if request.method == "POST":
        password = request.form["password"]
        if not check_password(g.user.id, password):
            return pages.get_password_error()
        boards.delete_board(board_id)
        return redirect(url_for("board.show_all"))
