from flask import (
    redirect,
    render_template,
    request,
    session,
    abort,
    url_for,
    g,
)
from app import app
import users
import boards
import topics
import posts
import groups
import memberships
from utils import check_csrf_token, check_board_access, check_password
import pages


@app.before_request
def load_session():
    print("load")
    g.user = None
    if "user_id" in session:
        g.user = users.get_user(session["user_id"])


@app.before_request
def test_csrf_token():
    if "user_id" not in session:
        return
    if request.method == "POST":
        if not check_csrf_token():
            abort(403)


@app.route("/")
def show_index():
    return render_template("index.html", boards=boards.get_boards())


@app.route("/login", methods=["GET", "POST"])
def log_in():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        message = "Väärä käyttäjätunnus tai salasana"
        return render_template("error.html", message=message)


@app.route("/logout")
def log_out():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        return pages.get_reserved_username_error()


@app.route("/users")
def show_users():
    return render_template("users.html", users=users.get_users())


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    user_groups = groups.get_user_groups(user_id)
    joinable_groups = groups.get_joinable_groups(user_id)
    return render_template(
        "user.html",
        user=user,
        groups=user_groups,
        joinable_groups=joinable_groups,
    )


@app.route("/user/<int:user_id>/remove", methods=["GET", "POST"])
def remove_user(user_id):
    if not g.user:
        return pages.get_login_error()
    if not (g.user.id == user_id or g.user.is_admin):
        return pages.get_access_error()
    if request.method == "GET":
        user = users.get_user(user_id)
        if not user:
            return pages.get_missing_error()
        return render_template("remove-user.html", user=user)
    if request.method == "POST":
        password = request.form["password"]
        if not check_password(g.user.id, password):
            return pages.get_password_error()
        users.remove_user(user_id)
        if user_id == g.user.id:
            return redirect(url_for("log_out"))
        return redirect(url_for("show_users"))


@app.route("/boards")
def show_boards():
    if not (g.user and g.user.is_admin):
        return pages.get_admin_error()
    return render_template("boards.html", boards=boards.get_boards())


@app.route("/board/add", methods=["GET", "POST"])
def add_board():
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
            return redirect(url_for("show_boards"))
        message = "Samanniminen alue on jo olemassa"
        return render_template("error.html", message=message), 409


@app.route("/board/<int:board_id>")
def show_board(board_id):
    if not check_board_access(board_id):
        return pages.get_access_error()
    board = boards.get_board(board_id)
    if not board:
        return pages.get_missing_error()
    board_topics = topics.get_topics(board_id)
    return render_template("board.html", board=board, topics=board_topics)


@app.route("/board/<int:board_id>/topic/add", methods=["GET", "POST"])
def add_topic(board_id):
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


@app.route("/topic/<int:topic_id>", methods=["GET", "POST"])
def show_topic(topic_id):
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


@app.route("/topic/<int:topic_id>/edit", methods=["GET", "POST"])
def edit_topic(topic_id):
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
        return redirect(url_for("show_topic", topic_id=topic_id))


@app.route("/topic/<int:topic_id>/remove", methods=["GET", "POST"])
def remove_topic(topic_id):
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
        return redirect(url_for("show_index"))


@app.route("/groups")
def show_groups():
    return render_template("groups.html", groups=groups.get_groups())


@app.route("/group/<int:group_id>", methods=["GET", "POST"])
def show_group(group_id):
    group = groups.get_group(group_id)
    if not group:
        return pages.get_missing_error()
    return render_template("group.html", group=group)


@app.route("/group/add", methods=["GET", "POST"])
def add_group():
    if not (g.user and g.user.is_admin):
        return pages.get_admin_error()
    if request.method == "GET":
        return render_template("add-group.html")
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        groups.add_group(title, description)
        return redirect(url_for("show_groups"))


@app.route("/group/<int:group_id>/join/<int:user_id>", methods=["POST"])
def add_membership(group_id, user_id):
    if not (g.user and g.user.is_admin):
        return pages.get_admin_error()
    memberships.add_membership(group_id, user_id)
    return redirect(url_for("show_user", user_id=user_id))


@app.route("/group/<int:group_id>/remove/<int:user_id>", methods=["POST"])
def remove_membership(group_id, user_id):
    if not (g.user and g.user.is_admin):
        return pages.get_admin_error()
    memberships.remove_membership(group_id, user_id)
    return redirect(url_for("show_user", user_id=user_id))
