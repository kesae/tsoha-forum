from sqlalchemy import text
from app import db


def get_board_topic(topic_id):
    sql = text(
        "SELECT t.id AS id, t.title AS title, board_id, b.title AS board_title "
        "FROM topics AS t JOIN boards AS b ON b.id=t.board_id WHERE t.id=:id"
    )
    result = db.session.execute(sql, {"id": topic_id})
    return result.fetchone()


def get_topics(board_id):
    sql = text("SELECT id, title FROM topics WHERE board_id=:board_id")
    result = db.session.execute(sql, {"board_id": board_id})
    return result.fetchall()


def add_topic(title, board_id):
    sql = text(
        "INSERT INTO topics (title,board_id) "
        "VALUES (:title,:board_id) RETURNING id"
    )
    params = {"title": title, "board_id": board_id}
    result = db.session.execute(sql, params)
    db.session.commit()
    return result.fetchone()[0]
