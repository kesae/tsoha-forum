from sqlalchemy import text, exc
from db import db


def add_membership(group_id, user_id):
    sql_string = """
        INSERT INTO
            memberships (group_id, user_id)
        VALUES
            (:group_id, :user_id);
    """
    sql = text(sql_string)
    params = {"group_id": group_id, "user_id": user_id}
    try:
        db.session.execute(sql, params)
        db.session.commit()
    except exc.IntegrityError:
        return False
    return True


def remove_membership(group_id, user_id):
    sql_string = """
        DELETE FROM
            memberships
        WHERE
            group_id = :group_id
            AND user_id = :user_id;
    """
    sql = text(sql_string)
    params = {"group_id": group_id, "user_id": user_id}
    db.session.execute(sql, params)
    db.session.commit()


def get_paginated_members(group_id, page=1, page_size=20):
    sql_string = """
        SELECT
            u.id id,
            u.username,
            u.is_admin
        FROM
            users u 
            JOIN
                memberships m 
                ON u.id = m.user_id
            JOIN
                groups g
                ON m.group_id = g.id
        WHERE
            g.id = :group_id
        ORDER BY
            u.username
        LIMIT
            :page_size
            OFFSET :page_size * (:page - 1);
    """
    sql = text(sql_string)
    result = db.session.execute(
        sql, {"group_id": group_id, "page": page, "page_size": page_size}
    )
    return result.fetchall()


def get_group_member_count(group_id):
    sql_string = """
        SELECT
            COUNT(*)
        FROM
            users u 
            JOIN
                memberships m 
                ON u.id = m.user_id
            JOIN
                groups g
                ON m.group_id = g.id
        WHERE
            g.id = :group_id;
    """
    sql = text(sql_string)
    result = db.session.execute(sql, {"group_id": group_id})
    return result.fetchone().count
