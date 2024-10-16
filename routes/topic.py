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
from utils import check_board_access, check_password
import pages


bp = Blueprint("topic", __name__)


@bp.route("/board/<int:board_id>/topic/add", methods=["GET", "POST"])
def add(board_id):
    if not check_board_access(board_id):
        return pages.get_access_error()
    user_id = session.get("user_id", None)
    if not user_id:
        return pages.get_login_error()
    if request.method == "GET":
        return render_template("add-topic.html", board_id=board_id)
    if request.method == "POST":
        board_id = int(request.form["board_id"])
        title = request.form["title"]
        content = request.form["content"]
        topic_id = topics.add_topic(user_id, title, board_id)
        if topic_id:
            posts.add_post(user_id, content, topic_id)
            return redirect(f"/board/{board_id}")
        return render_template(
            "error.html", message="Lähettäminen ei onnistunut"
        )


@bp.route("/topic/<int:topic_id>", methods=["GET", "POST"])
def show(topic_id):
    topic = topics.get_board_topic(topic_id)
    topic_posts = posts.get_posts(topic_id)
    if request.method == "GET":
        return render_template("topic.html", posts=topic_posts, topic=topic)
    if request.method == "POST":
        user_id = session.get("user_id")
        if not user_id:
            return pages.get_login_error()
        content = request.form["content"]
        posts.add_post(user_id, content, topic_id)
        return redirect(f"/topic/{topic_id}")


@bp.route("/topic/<int:topic_id>/edit", methods=["GET", "POST"])
def edit(topic_id):
    if not g.user:
        return pages.get_login_error()
    topic = topics.get_board_topic(topic_id)
    if not (g.user.id == topic.user_id or g.user.is_admin):
        return pages.get_access_error()
    if request.method == "GET":
        return render_template("edit-topic.html", topic=topic)
    if request.method == "POST":
        title = request.form["title"]
        topics.edit_title(topic_id, title)
        return redirect(url_for("topic.show", topic_id=topic_id))


@bp.route("/topic/<int:topic_id>/remove", methods=["GET", "POST"])
def remove(topic_id):
    if not g.user:
        return pages.get_login_error()
    topic = topics.get_board_topic(topic_id)
    if not (g.user.id == topic.user_id or g.user.is_admin):
        return pages.get_access_error()
    if request.method == "GET":
        return render_template("remove-topic.html", topic=topic)
    if request.method == "POST":
        password = request.form["password"]
        if not check_password(g.user.id, password):
            return pages.get_password_error()
        topics.remove_topic(topic_id)
        return redirect(url_for("index.show"))
