from flask import Blueprint
from markupsafe import escape_silent, Markup


bp = Blueprint("filters", __name__)


@bp.app_template_filter("make_safe_html")
def make_safe_html(text):
    safe_text = str(escape_silent(text))
    safe_html = safe_text.replace("\r\n", "<br/>").replace("\n", "<br/>")
    html_marked_safe = Markup(safe_html)
    return html_marked_safe
