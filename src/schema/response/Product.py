from marshmallow import fields
from src.schema.response import BaseResponse


# Product Schema Class
class ProductSchema(BaseResponse):

    name = fields.String(required=True)
    seller_id = fields.Integer(required=True)
    description = fields.String(required=True)
    category_id = fields.Integer(required=True)
    brand_id = fields.Integer(required=True)
    price = fields.Decimal(required=True, as_string=True)
    quantity = fields.Integer(required=True)
    discount_price = fields.Decimal(required=False, as_string=True)
    rating = fields.Integer(required=False)
