from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text, exc
from app import db


def users_exists():
    sql = text("SELECT id FROM users LIMIT 1")
    result = db.session.execute(sql)
    return bool(result.fetchone())


def register(username, password):
    password_hash = generate_password_hash(password)
    is_first = not users_exists()
    sql = text(
        "INSERT INTO users (username, password, is_admin)"
        "VALUES (:username, :password, :is_admin)"
    )
    params = {"username": username, "password": password_hash, "is_admin": is_first}
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
        return True
    return False


def logout():
    del session["user_id"]
