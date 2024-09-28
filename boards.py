from sqlalchemy import text
from app import db


def get_board(id):
    sql = text("SELECT id, title, description FROM boards WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()


def get_boards():
    sql_string = """
        SELECT
            b.id id,
            b.title title,
            b.description description,
            COUNT(DISTINCT t.id) topic_count,
            COUNT(p.id) post_count,
            MAX(created_at) latest_post_at 
        FROM
            boards b 
            LEFT JOIN
                topics t 
                ON b.id = t.board_id 
            LEFT JOIN
                posts p 
                ON t.id = p.topic_id 
        GROUP BY
            b.id;
    """
    sql = text(sql_string)
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
