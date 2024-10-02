from sqlalchemy import text
from app import db


def get_board_topic(topic_id):
    sql_string = """
        SELECT
            t.id AS id,
            t.title AS title,
            board_id,
            b.title AS board_title 
        FROM
            topics AS t 
            JOIN
                boards AS b 
                ON b.id = t.board_id 
        WHERE
            t.id = :id;
    """
    sql = text(sql_string)
    result = db.session.execute(sql, {"id": topic_id})
    return result.fetchone()


def get_topics(board_id):
    sql_string = """
        SELECT
            t.id id,
            t.title title,
            COUNT(p.id) post_count,
            MAX(p.created_at) latest_post_at 
        FROM
            topics t 
            LEFT JOIN
                posts p 
                ON t.id = topic_id 
        WHERE
            t.board_id = :board_id 
        GROUP BY
            t.id 
        ORDER BY
            latest_post_at ASC;
    """
    sql = text(sql_string)
    result = db.session.execute(sql, {"board_id": board_id})
    return result.fetchall()


def add_topic(title, board_id):
    sql_string = """
        INSERT INTO
            topics (title, board_id) 
        VALUES
            (
                :title, :board_id
            )
        RETURNING id;
    """
    sql = text(sql_string)
    params = {"title": title, "board_id": board_id}
    result = db.session.execute(sql, params)
    db.session.commit()
    return result.fetchone()[0]
