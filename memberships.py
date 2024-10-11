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
