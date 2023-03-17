from src.schema.response import BaseResponse
from marshmallow import fields


# Address schema class
class AddressSchema(BaseResponse):
    user_id = fields.Integer(required=True)
    street_address = fields.String(required=True)
    suburb = fields.String(required=True)
    state = fields.String(required=True)
    postcode = fields.String(required=True)
    default = fields.Boolean(required=False)
