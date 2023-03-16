
from flask_restx import fields

product_var: dict = {
    'name': fields.String(required=True, description='Product name'),
    'description': fields.String(required=False, description='Product description'),
    'category_id': fields.Integer(required=True, description='Product category ID'),
    'brand_id': fields.Integer(required=True, description='Product brand ID'),
    'price': fields.Fixed(required=True, description='Product price'),
    'quantity': fields.Integer(required=True, description='Product quantity', default=0)
}
product_update: dict = {
    'id': fields.Integer(required=True),
    'name': fields.String(description='Product name'),
    'description': fields.String(description='Product description'),
    'category_id': fields.Integer(description='Product category ID'),
    'brand_id': fields.Integer(description='Product brand ID'),
    'price': fields.Fixed(description='Product price'),
    'quantity': fields.Integer(description='Product quantity', default=0),
    'discount_price': fields.Integer(description='Product', required=False),
    'rating': fields.Integer(description='rating 0 to 5', required=False)

}
product_delete: dict = {
    'id': fields.Integer(required=True, description='Product ID', example=1)
}
