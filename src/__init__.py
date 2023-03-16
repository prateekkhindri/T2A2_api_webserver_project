from flask import Flask
from .connect_extension import connect_extension
from .connect_api import connect_blueprint
from src.cli.commands import db_commands


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    connect_extension(app)
    connect_blueprint(app)
    app.register_blueprint(db_commands)

    return app
