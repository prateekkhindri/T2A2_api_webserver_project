from marshmallow import fields
from src.utils.constants import EXCLUDED_FIELDS
from src.schema.response import BaseResponse
from src.schema.response.Product import ProductSchema


# Category Schema Class
class CategorySchema(BaseResponse):
    name = fields.String(required=True)
    description = fields.String(required=True)
    products = fields.Nested(ProductSchema(many=True, exclude=EXCLUDED_FIELDS))
