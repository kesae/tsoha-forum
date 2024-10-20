from sqlalchemy import text
from db import db


def count_topic_posts(topic_id):
    sql_string = """
        SELECT
            COUNT(*)
        FROM
            posts p
        WHERE
            p.topic_id = :topic_id;
    """
    sql = text(sql_string)
    result = db.session.execute(sql, {"topic_id": topic_id})
    return result.fetchone().count


def get_paginated_posts(topic_id, page=1, page_size=20):
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
            topic_id = :topic_id
        ORDER BY
            p.created_at,
            p.id
        LIMIT
            :page_size
            OFFSET :page_size * (:page - 1);
    """
    sql = text(sql_string)
    params = {"topic_id": topic_id, "page": page, "page_size": page_size}
    result = db.session.execute(sql, params)
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


def search_posts(user_id, query, page=1, page_size=20):
    sql_string = """
        SELECT
            p.id,
            p.user_id,
            content,
            created_at,
            edited_at,
            username
        FROM
            boards b 
            LEFT JOIN
                memberships m 
                ON b.access_group = m.group_id 
            LEFT JOIN
                GROUPS g 
                ON g.id = m.group_id 
            JOIN
                topics t 
                ON b.id = t.board_id 
            JOIN
                posts p 
                ON t.id = p.topic_id
            JOIN
                users u
                ON u.id = p.user_id 
        WHERE
            p.content LIKE :query
            AND
            (
                b.access_group IS NULL 
                OR m.user_id = :user_id
                OR EXISTS
                (   
                    SELECT
                        1
                    FROM
                        users u
                    WHERE
                        u.id = :user_id
                        AND u.is_admin
                )
            )
        ORDER BY
            p.created_at DESC,
            p.id DESC
        LIMIT
            :page_size
            OFFSET :page_size * (:page - 1);
    """
    sql = text(sql_string)
    params = {
        "user_id": user_id,
        "query": f"%{query}%",
        "page": page,
        "page_size": page_size,
    }
    result = db.session.execute(sql, params)
    return result.fetchall()


def count_search_posts(user_id, query):
    sql_string = """
        SELECT
            COUNT(*)
        FROM
            boards b 
            LEFT JOIN
                memberships m 
                ON b.access_group = m.group_id 
            LEFT JOIN
                GROUPS g 
                ON g.id = m.group_id 
            JOIN
                topics t 
                ON b.id = t.board_id 
            JOIN
                posts p 
                ON t.id = p.topic_id
        WHERE
            p.content LIKE :query
            AND
            (
                b.access_group IS NULL 
                OR m.user_id = :user_id
                OR EXISTS
                (   
                    SELECT
                        1
                    FROM
                        users u
                    WHERE
                        u.id = :user_id
                        AND u.is_admin
                )
            );
    """
    sql = text(sql_string)
    params = {
        "user_id": user_id,
        "query": f"%{query}%",
    }
    result = db.session.execute(sql, params)
    return result.fetchone().count


def get_post_location(post_id):
    sql_string = """
        SELECT
            t.id topic_id,
            COUNT(*)
        FROM
            topics t 
            JOIN
                posts p
                ON t.id = p.topic_id 
        WHERE
            t.id = 
            (
                SELECT
                    t.id id
            FROM
                topics t 
            JOIN
                posts p
                ON t.id = p.topic_id 
            WHERE
                p.id = :post_id
            )
            AND (p.created_at, p.id) < ((
                SELECT
                    created_at,
                    id
                FROM
                    posts
                WHERE
                    id = :post_id
            ))
        GROUP BY
            t.id;
    """
    sql = text(sql_string)
    params = {
        "post_id": post_id,
    }
    result = db.session.execute(sql, params)
    return result.fetchone()
