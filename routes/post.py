from flask import redirect, render_template, request, url_for, g, Blueprint
import posts
import errorpages
from utils import create_page_numbers

bp = Blueprint("post", __name__)


@bp.before_request
def check_access():
    if not g.user:
        return errorpages.get_no_login()


@bp.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
def edit(post_id):
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
    post = posts.get_post(post_id)
    if not post:
        return errorpages.get_page_missing()
    if not (g.user.id == post.user_id or g.user.is_admin):
        return errorpages.get_no_access()
    if request.method == "POST":
        posts.remove_post(post_id)
        return redirect(url_for("topic.show", topic_id=post.topic_id))


@bp.route("/posts/search")
def search():
    query = request.args.get("query")
    if not query:
        return render_template("search.html", results=None)
    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        return errorpages.get_page_missing()
    PAGE_SIZE = 20
    result_count = posts.count_search_posts(g.user.id, query)
    last_page = max(0, result_count - 1) // (PAGE_SIZE) + 1
    limited_page = min(max(1, page), last_page)
    if limited_page != page:
        return redirect(url_for("search.html", query=query, page=limited_page))
    page_numbers = create_page_numbers(page, last_page)
    results = posts.search_posts(g.user.id, query, page=page)
    return render_template(
        "search.html", results=results, page_numbers=page_numbers
    )
