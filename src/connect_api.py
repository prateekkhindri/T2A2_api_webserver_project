from flask_restx import Api


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

    api.init_app(app)
