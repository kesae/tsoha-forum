from os import getenv
from flask import Flask
from db import db
from routing import blueprints


def create_app():
    created_app = Flask(__name__)
    created_app.secret_key = getenv("SECRET_KEY")
    created_app.config["SQLALCHEMY_DATABASE_URI"] = getenv(
        "DATABASE_URL"
    ).replace("s://", "sql://", 1)
    db.init_app(created_app)
    for blueprint in blueprints:
        created_app.register_blueprint(blueprint)
    return created_app


if __name__ == "__main__":
    app = create_app()
