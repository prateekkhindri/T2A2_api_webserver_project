from flask import Flask
from .connect_extension import connect_extension
from .connect_api import connect_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    connect_extension(app)
    connect_blueprint(app)

    return app
