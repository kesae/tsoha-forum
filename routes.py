from flask import redirect, render_template, request, session
from app import app
import users
import boards
import topics
import posts


@app.route("/")
def index():
    return render_template(
        "index.html", boards=boards.get_boards(), is_admin=users.is_admin()
    )


@app.route("/login", methods=["GET", "POST"])
def login():
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
def logout():
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
        return render_template("error.html", message="Rekisteröinti ei onnistunut")


@app.route("/edit_boards")
def edit_boards():
    if not users.is_admin():
        return render_template("error.html", message="Pääsy estetty"), 403
    return render_template("edit_boards.html", boards=boards.get_boards())


@app.route("/new_board", methods=["GET", "POST"])
def new_board():
    if not users.is_admin():
        return render_template("error.html", message="Pääsy estetty"), 403
    if request.method == "GET":
        return render_template("new_board.html")
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        boards.add_board(title, description)
        return redirect("/edit_boards")


@app.route("/board/<int:id>")
def board(id):
    board_data = boards.get_board(id)
    if not board_data:
        return render_template("error.html", message="Sivua ei löydy")
    board_topics = topics.get_topics(id)
    return render_template("board.html", board=board_data, topics=board_topics)


@app.route("/new_topic/<int:board_id>", methods=["GET", "POST"])
def new_topic(board_id):
    user_id = session.get("user_id", None)
    if not user_id:
        return render_template("error.html", message="Toiminto vaatii kirjautumisen")
    if request.method == "GET":
        return render_template("new_topic.html", board_id=board_id)
    if request.method == "POST":
        board_id = int(request.form["board_id"])
        title = request.form["title"]
        content = request.form["content"]
        topic_id = topics.add_topic(title, board_id)
        if topic_id:
            posts.add_post(user_id, content, topic_id)
            return redirect(f"/board/{board_id}")
        return render_template("error.html", message="Lähettäminen ei onnistunut")


@app.route("/topic/<int:topic_id>", methods=["GET", "POST"])
def topic(topic_id):
    topic_data = topics.get_board_topic(topic_id)
    topic_posts = posts.get_posts(topic_id)
    if request.method == "GET":
        return render_template("topic.html", posts=topic_posts, topic=topic_data)
    if request.method == "POST":
        user_id = session.get("user_id")
        if not user_id:
            return render_template(
                "error.html", message="Toiminto vaatii kirjautumisen"
            )
        content = request.form["content"]
        posts.add_post(user_id, content, topic_id)
        return redirect(f"/topic/{topic_id}")
