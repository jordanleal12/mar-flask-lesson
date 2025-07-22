import os
from flask import Flask
from init import db


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    db.init_app(app)

    from controllers import controller_blueprints

    for controller in controller_blueprints:
        app.register_blueprint(controller)

    return app
