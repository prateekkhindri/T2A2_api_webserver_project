from flask_restx import fields


address_create = {
    'street_address': fields.String(required=True),
    'suburb': fields.String(required=True),
    'state': fields.String(required=True),
    'postcode': fields.String(required=True),
    'default': fields.Boolean(required=False)
}

address_update = {
    'street_address': fields.String(required=True),
    'suburb': fields.String(required=True),
    'state': fields.String(required=True),
    'postcode': fields.String(required=True)
}
