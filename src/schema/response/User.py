from marshmallow import fields
from src.schema.response import BaseResponse

# User Schema Class


class UserSchema(BaseResponse):
    id = fields.Integer(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    username = fields.String(required=True)
    phone_number = fields.String(required=True)
    is_admin = fields.Boolean(required=False)
    is_seller = fields.Boolean(required=False)
