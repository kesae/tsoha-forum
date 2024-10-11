from sqlalchemy import text, exc
from db import db


def get_groups():
    sql_string = """
        SELECT
            g.id id,
            g.title title,
            g.description description,
            COUNT(DISTINCT m.user_id) member_count
        FROM
            groups g 
            LEFT JOIN
                memberships m 
                ON g.id = m.group_id 
        GROUP BY
            g.id;
    """
    sql = text(sql_string)
    result = db.session.execute(sql)
    return result.fetchall()


def get_user_groups(user_id):
    sql_string = """
        SELECT
            g.id id,
            g.title title,
            g.description description
        FROM
            groups g 
            LEFT JOIN
                memberships m 
                ON g.id = m.group_id 
        WHERE
            m.user_id = :user_id;
    """
    sql = text(sql_string)
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()


def get_joinable_groups(user_id):
    sql_string = """
        SELECT
            g.id id,
            g.title title,
            g.description description 
        FROM
            users u 
            CROSS JOIN
                GROUPS g 
            LEFT JOIN
                memberships m 
                ON g.id = m.group_id 
                AND u.id = m.user_id 
        WHERE
            u.id = :user_id 
            AND m.group_id IS NULL;
    """
    sql = text(sql_string)
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()


def get_group(group_id):
    sql_string = """
        SELECT
            g.id id,
            g.title title,
            g.description description,
            COUNT(DISTINCT m.user_id) member_count
        FROM
            groups g
            LEFT JOIN
                memberships m
                ON g.id = m.group_id
        WHERE
            id = :id
        GROUP BY
            g.id
    """
    sql = text(sql_string)
    result = db.session.execute(sql, {"id": group_id})
    return result.fetchone()


def add_group(title, description):
    sql_string = """
        INSERT INTO
            groups (title, description) 
        VALUES
            (:title, :description);
    """
    sql = text(sql_string)
    params = {"title": title, "description": description}
    try:
        db.session.execute(sql, params)
        db.session.commit()
    except exc.IntegrityError:
        return False
    return True


def add_membership(group_id, user_id):
    sql_string = """
        INSERT INTO
            memberships (group_id, user_id)
        VALUES
            (:group_id, user_id);
    """
    sql = text(sql_string)
    params = {"group_id": group_id, "user_id": user_id}
    try:
        db.session.execute(sql, params)
        db.session.commit()
    except exc.IntegrityError:
        return False
    return True
