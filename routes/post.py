from flask import redirect, render_template, request, url_for, g, Blueprint
import posts
import errorpages


bp = Blueprint("post", __name__)


@bp.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
def edit(post_id):
    if not g.user:
        return errorpages.get_no_login()
    post = posts.get_post(post_id)
    if not post:
        return errorpages.get_page_missing()
    if not (g.user.id == post.user_id or g.user.is_admin):
        return errorpages.get_no_access()
    if request.method == "GET":
        return render_template("edit-post.html", post=post)
    if request.method == "POST":
        content = request.form["content"]
        if not 5 <= len(content) <= 10_000:
            return errorpages.get_post_length()
        posts.edit_post(post_id, content)
        return redirect(url_for("topic.show", topic_id=post.topic_id))


@bp.route("/post/<int:post_id>/remove", methods=["POST"])
def remove(post_id):
    if not g.user:
        return errorpages.get_no_login()
    post = posts.get_post(post_id)
    if not post:
        return errorpages.get_page_missing()
    if not (g.user.id == post.user_id or g.user.is_admin):
        return errorpages.get_no_access()
    if request.method == "POST":
        posts.remove_post(post_id)
        return redirect(url_for("topic.show", topic_id=post.topic_id))
