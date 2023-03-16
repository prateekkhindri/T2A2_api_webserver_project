from marshmallow import Schema, fields

# Base Schema Class


class BaseResponse(Schema):

    id = fields.Integer(required=True)
    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)
