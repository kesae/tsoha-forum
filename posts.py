from sqlalchemy import text
from db import db


def get_posts(topic_id):
    sql_string = """
        SELECT
            p.id id,
            user_id,
            content,
            created_at,
            edited_at,
            username
        FROM
            posts p
        JOIN
            users u
            ON u.id = p.user_id
        WHERE
            topic_id = :topic_id;
    """
    sql = text(sql_string)
    result = db.session.execute(sql, {"topic_id": topic_id})
    return result.fetchall()


def get_post(post_id):
    sql_string = """
        SELECT
            id,
            user_id,
            content,
            topic_id,
            created_at,
            edited_at 
        FROM
            posts 
        WHERE
            id = :id;
    """
    sql = text(sql_string)
    result = db.session.execute(sql, {"id": post_id})
    return result.fetchone()


def add_post(user_id, content, topic_id):
    sql_string = """
        INSERT INTO
            posts (user_id, content, topic_id) 
        VALUES
            (:user_id, :content, :topic_id);
    """
    sql = text(sql_string)
    params = {"user_id": user_id, "content": content, "topic_id": topic_id}
    db.session.execute(sql, params)
    db.session.commit()


def edit_post(post_id, content):
    sql_string = """
        UPDATE
            posts
        SET
            content = :content,
            edited_at = NOW() 
        WHERE
            id = :id;
    """
    sql = text(sql_string)
    params = {"id": post_id, "content": content}
    db.session.execute(sql, params)
    db.session.commit()


def remove_post(post_id):
    sql_string = """
        DELETE FROM
            posts
        WHERE
            id = :id;
    """
    sql = text(sql_string)
    db.session.execute(sql, {"id": post_id})
    db.session.commit()
