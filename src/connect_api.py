from flask_restx import Api
from src.controllers.auth_controller import api as auth


authorizations = {
    'Token Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


api = Api(
    version='1.0',
    title='Sneaker Connect',
    description='2-Sided Marketplace API',
    security='Token Auth',
    authorizations=authorizations
)


def connect_blueprint(app):
    api.add_namespace(auth, path="/auth/")

    api.init_app(app)
