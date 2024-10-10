from sqlalchemy import text, exc
from app import db


def get_board(board_id):
    sql_string = """
        SELECT
            id,
            title,
            description 
        FROM
            boards 
        WHERE
            id = :id;
    """
    sql = text(sql_string)
    result = db.session.execute(sql, {"id": board_id})
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


def user_has_access(user_id, board_id):
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
        OR 
        (
            SELECT
                EXISTS
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
        )
        AS
            has_access;
    """
    sql = text(sql_string)
    params = {"user_id": user_id, "board_id": board_id}
    result = db.session.execute(sql, params)
    return result.fetchone().has_access
