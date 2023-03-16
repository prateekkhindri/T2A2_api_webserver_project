from marshmallow import fields
from src.utils.constants import EXCLUDED_FIELDS
from src.schema.response.Product import ProductSchema
from src.schema.response import BaseResponse


# Brand Schema Class
class BrandSchema(BaseResponse):

    name = fields.String(required=True)
    description = fields.String(required=True)
    products = fields.Nested(ProductSchema(many=True, exclude=EXCLUDED_FIELDS))
