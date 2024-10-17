from sqlalchemy import text, exc
from db import db


def get_board(board_id):
    sql_string = """
        SELECT
            b.id,
            b.title title,
            b.description,
            b.access_group,
            g.title access_title
        FROM
            boards b
            LEFT JOIN
                groups g
                ON b.access_group = g.id
        WHERE
            b.id = :id;
    """
    sql = text(sql_string)
    result = db.session.execute(sql, {"id": board_id})
    return result.fetchone()


def get_user_boards(user_id):
    sql_string = """
        SELECT
            b.id id,
            b.title title,
            b.description description,
            access_group,
            g.title access_title,
            COUNT(DISTINCT t.id) topic_count,
            COUNT(DISTINCT p.id) post_count,
            MAX(created_at) latest_post_at 
        FROM
            boards b 
            LEFT JOIN
                memberships m 
                ON b.access_group = m.group_id 
            LEFT JOIN
                GROUPS g 
                ON g.id = m.group_id 
            LEFT JOIN
                topics t 
                ON b.id = t.board_id 
            LEFT JOIN
                posts p 
                ON t.id = p.topic_id 
        WHERE
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
        GROUP BY
        (b.id, g.id);
    """
    sql = text(sql_string)
    params = {"user_id": user_id}
    result = db.session.execute(sql, params)
    return result.fetchall()


def add_board(title, description, access_group):
    sql_string = """
        INSERT INTO
            boards (title, description,access_group) 
        VALUES
            (:title, :description, :access_group);
    """
    sql = text(sql_string)
    params = {
        "title": title,
        "description": description,
        "access_group": access_group,
    }
    try:
        db.session.execute(sql, params)
        db.session.commit()
    except exc.IntegrityError:
        return False
    return True


def edit_board(board_id, title, description, access_group):
    sql_string = """
        UPDATE
            boards 
        SET
            title = :title,
            description = :description,
            access_group = :access_group 
        WHERE
            id = :id;

    """
    sql = text(sql_string)
    params = {
        "id": board_id,
        "title": title,
        "description": description,
        "access_group": access_group,
    }
    try:
        db.session.execute(sql, params)
        db.session.commit()
    except exc.IntegrityError:
        return False
    return True


def delete_board(board_id):
    sql_string = """
        DELETE
        FROM
            boards 
        WHERE
            id = :id;
    """
    sql = text(sql_string)
    db.session.execute(sql, {"id": board_id})
    db.session.commit()


def nonadmin_has_access(user_id, board_id):
    sql_string = """
        SELECT
        (
            SELECT
                b.access_group IS NULL 
            FROM
                boards b 
            WHERE
                b.id = :board_id
        ) 
        OR EXISTS
        (
            SELECT
                1 
            FROM
                boards b 
                JOIN
                    memberships m 
                    ON b.access_group = m.group_id 
            WHERE
                m.user_id = :user_id 
                AND b.id = :board_id
        )
        AS
            has_access;
    """
    sql = text(sql_string)
    params = {"user_id": user_id, "board_id": board_id}
    result = db.session.execute(sql, params)
    return result.fetchone().has_access
