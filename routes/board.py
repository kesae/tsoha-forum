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
from utils import (
    check_board_access,
    get_boards,
    check_password,
    create_page_numbers,
)
import errorpages


bp = Blueprint("board", __name__)


@bp.route("/boards")
def show_all():
    if not (g.user and g.user.is_admin):
        return errorpages.get_no_admin()
    return render_template("boards.html", boards=get_boards())


@bp.route("/board/add", methods=["GET", "POST"])
def add():
    if not (g.user and g.user.is_admin):
        return errorpages.get_no_admin()
    if request.method == "GET":
        access_groups = groups.get_groups()
        return render_template("add-board.html", access_groups=access_groups)
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        access_string = request.form["access_group"]
        if not 5 <= len(title) <= 30:
            return errorpages.get_title_length()
        if not len(description) <= 100:
            return errorpages.get_long_description()
        try:
            access_group = int(access_string)
        except ValueError:
            abort(403)
        access_group = None if access_group < 1 else access_group
        if boards.add_board(title, description, access_group):
            return redirect(url_for("board.show_all"))
        return errorpages.get_reserved_board()


@bp.route("/board/<int:board_id>")
def show(board_id):
    PAGE_SIZE = 20
    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        return errorpages.get_page_missing()
    if not check_board_access(board_id):
        return errorpages.get_no_access()
    board = boards.get_board(board_id)
    if not board:
        return errorpages.get_page_missing()
    topic_count = topics.get_board_topic_count(board_id)
    print("Topic count", topic_count)
    last_page = max(0, topic_count - 1) // (PAGE_SIZE) + 1
    print("Last page", last_page)
    limited_page = min(max(1, page), last_page)
    if limited_page != page:
        return redirect(
            url_for("board.show", board_id=board_id, page=limited_page)
        )
    page_numbers = create_page_numbers(page, last_page)
    board_topics = topics.get_paginated_topics(board_id, page)
    return render_template(
        "board.html",
        board=board,
        topics=board_topics,
        page_numbers=page_numbers,
    )


@bp.route("/board/<int:board_id>/edit", methods=["GET", "POST"])
def edit(board_id):
    if not (g.user and g.user.is_admin):
        return errorpages.get_no_admin()
    board = boards.get_board(board_id)
    if not board:
        return errorpages.get_page_missing()
    if request.method == "GET":
        access_groups = groups.get_groups()
        return render_template(
            "edit-board.html", board=board, access_groups=access_groups
        )
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        access_string = request.form["access_group"]
        if not 5 <= len(title) <= 30:
            return errorpages.get_title_length()
        if not len(description) <= 100:
            return errorpages.get_long_description()
        try:
            access_group = int(access_string)
        except ValueError:
            abort(403)
        access_group = None if access_group < 1 else access_group
        if boards.edit_board(board_id, title, description, access_group):
            return redirect(url_for("board.show_all"))
        return errorpages.get_reserved_board()


@bp.route("/board/<int:board_id>/remove", methods=["GET", "POST"])
def remove(board_id):
    if not (g.user and g.user.is_admin):
        return errorpages.get_no_admin()
    board = boards.get_board(board_id)
    if not board:
        return errorpages.get_page_missing()
    if request.method == "GET":
        return render_template("remove-board.html", board=board)
    if request.method == "POST":
        password = request.form["password"]
        if not check_password(g.user.id, password):
            return errorpages.get_wrong_password()
        boards.delete_board(board_id)
        return redirect(url_for("board.show_all"))
