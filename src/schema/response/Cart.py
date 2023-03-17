from flask_restx import fields
from src.schema.response import BaseResponse
from src.utils.constants import EXCLUDED_FIELDS
from src.schema.response.User import UserSchema
from src.schema.response.Product import ProductSchema


# CartItem Schema Class
class CartItemSchema(BaseResponse):

    excluded_fields = EXCLUDED_FIELDS.copy()
    excluded_fields.extend(
        ['quantity', 'brand_id', 'description', 'category_id'])
    quantity = fields.Integer(required=True)
    product = fields.Nested(ProductSchema(exclude=excluded_fields))
    cart_id = fields.Integer(required=True)


# Cart Schema Class
class CartSchema(BaseResponse):

    user_excluded_fields = EXCLUDED_FIELDS.copy()
    user_excluded_fields.extend(['password', 'is_admin'])
    owner = fields.Nested(UserSchema(exclude=user_excluded_fields))
    items = fields.Nested(CartItemSchema(many=True, exclude=EXCLUDED_FIELDS))
