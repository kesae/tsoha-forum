from sqlalchemy import text
from app import db


def get_posts(topic_id):
    sql = text(
        "SELECT id, user_id, content, created_at, edited_at "
        "FROM posts WHERE topic_id=:topic_id"
    )
    result = db.session.execute(sql, {"topic_id": topic_id})
    return result.fetchall()


def add_post(user_id, content, topic_id):
    sql = text(
        "INSERT INTO posts (user_id,content,topic_id) "
        "VALUES (:user_id,:content,:topic_id)"
    )
    params = {"user_id": user_id, "content": content, "topic_id": topic_id}
    db.session.execute(sql, params)
    db.session.commit()
