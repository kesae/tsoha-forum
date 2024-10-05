from flask import redirect, render_template, request, session, abort, url_for
from app import app
import users
import boards
import topics
import posts
import groups
from utils import check_csrf_token, check_board_access


@app.route("/")
def show_index():
    return render_template(
        "index.html", boards=boards.get_boards(), is_admin=users.is_admin()
    )


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
        return render_template(
            "error.html", message="Rekisteröinti ei onnistunut"
        )


@app.route("/boards")
def show_boards():
    if not users.is_admin():
        return render_template("error.html", message="Pääsy estetty"), 403
    return render_template("boards.html", boards=boards.get_boards())


@app.route("/board/add", methods=["GET", "POST"])
def add_board():
    if not users.is_admin():
        return render_template("error.html", message="Pääsy estetty"), 403
    if request.method == "GET":
        access_groups = groups.get_groups()
        return render_template("add-board.html", access_groups=access_groups)
    if request.method == "POST":
        if not check_csrf_token():
            abort(403)
        title = request.form["title"]
        description = request.form["description"]
        access_group = request.form["access_group"]
        boards.add_board(title, description, access_group)
        return redirect(url_for("show_boards"))


@app.route("/board/<int:board_id>")
def show_board(board_id):
    if not check_board_access(board_id):
        abort(403)
    board = boards.get_board(board_id)
    if not board:
        return render_template("error.html", message="Sivua ei löydy")
    board_topics = topics.get_topics(board_id)
    return render_template("board.html", board=board, topics=board_topics)


@app.route("/board/<int:board_id>/topic/add", methods=["GET", "POST"])
def add_topic(board_id):
    if not check_board_access(board_id):
        abort(403)
    user_id = session.get("user_id", None)
    if not user_id:
        return render_template(
            "error.html", message="Toiminto vaatii kirjautumisen"
        )
    if request.method == "GET":
        return render_template("add-topic.html", board_id=board_id)
    if request.method == "POST":
        if not check_csrf_token():
            abort(403)
        board_id = int(request.form["board_id"])
        title = request.form["title"]
        content = request.form["content"]
        topic_id = topics.add_topic(title, board_id)
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
        if not check_csrf_token():
            abort(403)
        user_id = session.get("user_id")
        if not user_id:
            return render_template(
                "error.html", message="Toiminto vaatii kirjautumisen"
            )
        content = request.form["content"]
        posts.add_post(user_id, content, topic_id)
        return redirect(f"/topic/{topic_id}")


@app.route("/groups")
def show_groups():
    return render_template("groups.html", groups=groups.get_groups())


@app.route("/group/<int:group_id>", methods=["GET", "POST"])
def show_group(group_id):
    group = groups.get_group(group_id)
    if not group:
        return render_template("error.html", message="Sivua ei löydy")
    return render_template("group.html", group=group)


@app.route("/group/add", methods=["GET", "POST"])
def add_group():
    if not users.is_admin():
        return render_template("error.html", message="Pääsy estetty"), 403
    if request.method == "GET":
        return render_template("add-group.html")
    if request.method == "POST":
        if not check_csrf_token():
            abort(403)
        title = request.form["title"]
        description = request.form["description"]
        groups.add_group(title, description)
        return redirect(url_for("show_groups"))
