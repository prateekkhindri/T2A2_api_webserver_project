from flask import request
from flask_restx import Namespace, Resource, fields
from src.utils.token_required import token_required
from src.models.Cart import Cart
from src.models.CartItem import CartItem
from src.utils import remove_space
from src.utils.constants import EXCLUDED_FIELDS
from src.schema.response.Cart import CartSchema, CartItemSchema
from src.extension import session
from src.utils.responses import success_response, error_response
from src.validators.cart import CartValidators
from src.models.Product import Product


api = Namespace('cart', description='Cart Related Operations')

cart_item_model = api.model('CartItem', {
    'product_id': fields.Integer(required=True, description='Product ID'),
    'quantity': fields.Integer(required=True, description='Product quantity', default=1),
})


# Endpoint to get a users cart
@api.route('')
class CartView(Resource):
    @token_required
    def get(self):
        cart_schema = CartSchema(exclude=EXCLUDED_FIELDS)
        user_id = session.current_user.get('id')

        # The query below is intended to retrieve the Cart object for the current user, based on the user_id value stored in the session
        cart = Cart.query.filter_by(user_id=user_id).first()

        if not cart:
            error_response['message'] = 'Cart not found'
            return error_response, 404

        cart_data = cart_schema.dump(cart)
        cart_item_schema = CartItemSchema(exclude=EXCLUDED_FIELDS, many=True)

        # The query below is intended to retrieve all CartItem objects that belong to a specific Cart object, which can be used to display the items in the user's cart or perform operations on the items
        cart_items = CartItem.query.filter_by(
            cart_id=cart.id).all()
        cart_item_data = cart_item_schema.dump(cart_items)
        cart_data.update({"cart_items": cart_item_data})

        success_response['message'] = 'Cart successfully fetched'
        success_response['data'] = {
            'cart': cart_data
        }
        return success_response, 200

    # Endpoint to add items to a users cart
    @token_required
    @api.expect(cart_item_model)
    def post(self):
        request_data = request.get_json()
        CartValidators.validate_item(request_data)
        request_data = remove_space(request_data)
        user_id = session.current_user.get('id')

        # The query below is intended to retrieve the Cart object for the current user, based on the user_id value stored in the session
        cart = Cart.query.filter_by(user_id=user_id).first()

        if not cart:
            new_cart = Cart(user_id=user_id)
            new_cart.save()
            success_response['message'] = "Cart has been successfully created"
            cart = new_cart

        # The query below is is intended to retrieve a specific CartItem object from a specific Cart, based on the cart_id and product_id values. Each CartItem represents a specific Product object that has been added to the specified Cart, and that the CartItem object contains a product_id field that links it to the Product object.
        cart_item = CartItem.query.filter_by(
            cart_id=cart.id, product_id=request_data.get('product_id')).first()
        product = Product.find_by_id(request_data.get('product_id'))

        if product.seller_id == user_id:
            error_response['message'] = 'You cannot add your own product to the cart'
            return error_response, 400

        request_data.update({'cart_id': cart.id})
        if cart_item:
            updated_quantity = product.quantity - request_data.get('quantity')
            request_data['quantity'] += cart_item.quantity
            CartValidators.validate_item(request_data)
            cart_item.update(request_data)
            product.update({'quantity': updated_quantity})
        else:
            new_cart_item = CartItem(**request_data)
            new_cart_item.save()
            new_quantity = product.quantity - request_data.get('quantity')
            product.update({'quantity': new_quantity})
        cart_schema = CartSchema(exclude=EXCLUDED_FIELDS)
        success_response['message'] = f'Item successfully added to the cart'
        success_response['data'] = {
            'cart': cart_schema.dump(cart)
        }
        return success_response, 201


# Endpoint to delete an item from the cart
@api.route('items/<int:cart_item_id>')
class CartItemView(Resource):
    @token_required
    def delete(self, cart_item_id):
        cart_schema = CartSchema(exclude=EXCLUDED_FIELDS)
        user_id = request.decoded_token['user']['id']

        # The query below is intended to retrieve the Cart object for the user who makes the request, based on the user_id value stored in the JWT. The Cart model has a user_id field that is used to associate the cart with a user
        cart = Cart.query.filter_by(user_id=user_id).first()

        # The query below is intended to retrieve a specific CartItem object from a specific Cart, based on the id and cart_id values
        cart_item = CartItem.query.filter_by(
            id=cart_item_id, cart_id=cart.id).first()

        if not cart_item:
            error_response['message'] = 'Cart Item not found'
            return error_response, 404

        product = Product.find_by_id(cart_item.product_id)
        quantity = product.quantity + cart_item.quantity
        product.update({'quantity': quantity})
        cart_item.delete()

        success_response['message'] = 'Item successfully removed from the cart'
        success_response['data'] = {
            'cart': cart_schema.dump(cart)
        }

        return success_response, 200
