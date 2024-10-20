from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text, exc
from db import db
from utils import set_csrf_token


def users_exist():
    sql = text("SELECT id FROM users LIMIT 1")
    result = db.session.execute(sql)
    return bool(result.fetchone())


def register(username, password):
    password_hash = generate_password_hash(password)
    is_first = not users_exist()
    sql_string = """
        INSERT INTO
            users (username, password, is_admin) 
        VALUES
            (:username, :password, :is_admin);
    """
    sql = text(sql_string)
    params = {
        "username": username,
        "password": password_hash,
        "is_admin": is_first,
    }
    try:
        db.session.execute(sql, params)
        db.session.commit()
    except exc.IntegrityError:
        return False
    return True


def login(username, password):
    sql = text("SELECT id, password FROM users where username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user and check_password_hash(user.password, password):
        session["user_id"] = user.id
        set_csrf_token()
        return True
    return False


def get_user(user_id):
    sql_string = """
        SELECT
            id, username, is_admin
        FROM
            users
        WHERE
            id = :id;
    """
    sql = text(sql_string)
    params = {"id": user_id}
    result = db.session.execute(sql, params)
    return result.fetchone()


def get_password_hash(user_id):
    sql_string = """
        SELECT
            password
        FROM
            users
        WHERE
            id = :id;
    """
    sql = text(sql_string)
    result = db.session.execute(sql, {"id": user_id})
    return result.fetchone()


def get_user_count():
    sql_string = """
        SELECT
            COUNT(*)
        FROM
            users
    """
    sql = text(sql_string)
    result = db.session.execute(sql)
    return result.fetchone().count


def get_users():
    sql_string = """
        SELECT
            id, username, is_admin
        FROM
            users
    """
    sql = text(sql_string)
    result = db.session.execute(sql)
    return result.fetchall()


def get_paginated_users(page=1, page_size=20):
    sql_string = """
        SELECT
            id, username, is_admin
        FROM
            users
        ORDER BY
            username,
            id
        LIMIT
            :page_size
            OFFSET :page_size * (:page - 1);
    """
    sql = text(sql_string)
    params = {"page": page, "page_size": page_size}
    result = db.session.execute(sql, params)
    return result.fetchall()


def logout():
    del session["user_id"]
