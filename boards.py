from sqlalchemy import text
from app import db


def get_board(id):
    sql = text("SELECT id, title, description FROM boards WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()


def get_boards():
    sql = text("SELECT id, title, description FROM boards")
    result = db.session.execute(sql)
    return result.fetchall()


def add_board(title, description):
    sql = text(
        "INSERT INTO boards (title, description) "
        "VALUES (:title, :description)"
    )
    params = {"title": title, "description": description}
    db.session.execute(sql, params)
    db.session.commit()
