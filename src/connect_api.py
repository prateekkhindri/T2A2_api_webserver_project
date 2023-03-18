from flask_restx import Api
from src.controllers.auth_controller import api as auth
from src.controllers.users_controller import api as user
from src.controllers.products_controller import api as product
from src.controllers.brands_controller import api as brand
from src.controllers.categories_controller import api as category
from src.controllers.carts_controller import api as cart
from src.controllers.addresses_controller import api as address


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
    api.add_namespace(user, path="/user/")
    api.add_namespace(product, path="/product/")
    api.add_namespace(brand, path="/brand/")
    api.add_namespace(category, path="/category/")
    api.add_namespace(cart, path="/cart/")
    api.add_namespace(address, path="/address/")

    api.init_app(app)
