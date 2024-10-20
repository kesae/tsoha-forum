from flask import (
    redirect,
    render_template,
    request,
    session,
    url_for,
    g,
    Blueprint,
)
import topics
import posts
from utils import check_board_access, check_password, create_page_numbers
import errorpages


bp = Blueprint("topic", __name__)


@bp.route("/board/<int:board_id>/topic/add", methods=["GET", "POST"])
def add(board_id):
    if not check_board_access(board_id):
        return errorpages.get_no_access()
    user_id = session.get("user_id", None)
    if not user_id:
        return errorpages.get_no_login()
    if request.method == "GET":
        return render_template("add-topic.html", board_id=board_id)
    if request.method == "POST":
        board_id = int(request.form["board_id"])
        title = request.form["title"]
        content = request.form["content"]
        if not 5 <= len(title) <= 30:
            return errorpages.get_title_length()
        if not 5 <= len(content) <= 10_000:
            return errorpages.get_post_length()
        topic_id = topics.add_topic(user_id, title, board_id)
        if topic_id:
            posts.add_post(user_id, content, topic_id)
            return redirect(f"/board/{board_id}")
        return render_template(
            "error.html", message="Lähettäminen ei onnistunut"
        )


@bp.route("/topic/<int:topic_id>", methods=["GET", "POST"])
def show(topic_id):
    page_size = 20
    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        return errorpages.get_page_missing()
    post_count = posts.count_topic_posts(topic_id)
    last_page = max(0, post_count - 1) // (page_size) + 1
    limited_page = min(max(1, page), last_page)
    if limited_page != page:
        return redirect(
            url_for("topic.show", topic_id=topic_id, page=limited_page)
        )
    page_numbers = create_page_numbers(page, last_page)
    topic = topics.get_board_topic(topic_id)
    topic_posts = posts.get_paginated_posts(
        topic_id, page, page_size=page_size
    )
    if request.method == "GET":
        return render_template(
            "topic.html",
            posts=topic_posts,
            topic=topic,
            page_numbers=page_numbers,
        )
    if request.method == "POST":
        user_id = session.get("user_id")
        if not user_id:
            return errorpages.get_no_login()
        content = request.form["content"]
        if not 5 <= len(content) <= 10_000:
            return errorpages.get_post_length()
        posts.add_post(user_id, content, topic_id)
        return redirect(f"/topic/{topic_id}")


@bp.route("/topic/<int:topic_id>/edit", methods=["GET", "POST"])
def edit(topic_id):
    if not g.user:
        return errorpages.get_no_login()
    topic = topics.get_board_topic(topic_id)
    if not (g.user.id == topic.user_id or g.user.is_admin):
        return errorpages.get_no_access()
    if request.method == "GET":
        return render_template("edit-topic.html", topic=topic)
    if request.method == "POST":
        title = request.form["title"]
        if not 5 <= len(title) <= 30:
            return errorpages.get_title_length()
        topics.edit_title(topic_id, title)
        return redirect(url_for("topic.show", topic_id=topic_id))


@bp.route("/topic/<int:topic_id>/remove", methods=["GET", "POST"])
def remove(topic_id):
    if not g.user:
        return errorpages.get_no_login()
    topic = topics.get_board_topic(topic_id)
    if not (g.user.id == topic.user_id or g.user.is_admin):
        return errorpages.get_no_access()
    if request.method == "GET":
        return render_template("remove-topic.html", topic=topic)
    if request.method == "POST":
        password = request.form["password"]
        if not check_password(g.user.id, password):
            return errorpages.get_wrong_password()
        topics.remove_topic(topic_id)
        return redirect(url_for("index.show"))
