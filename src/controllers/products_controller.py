from flask_restx import Resource, Namespace
from src.utils.responses import success_response, error_response
from src.schema.response.Product import ProductSchema
from src.models.Product import Product
from src.utils.constants import EXCLUDED_FIELDS


api = Namespace('products', description='Product Related Operations')


search_parser = api.parser()
search_parser.add_argument('name', required=False,
                           type=str, help="Search by the product name")


# Endpoint to get a single product
@api.route("<int:id>/")
class ProductSingleView(Resource):
    def get(self, id):
        product_schema = ProductSchema(exclude=EXCLUDED_FIELDS)
        product = Product.find_by_id(id)
        if product:
            product_data = product_schema.dump(product)
            success_response['message'] = "Product found"
            success_response['data'] = product_data
            return success_response, 200
        error_response['message'] = "Product not found"
        return error_response, 404


# Endpoint to get all products
@api.route("")
class ProductView(Resource):
    def get(self):
        products_schema = ProductSchema(exclude=EXCLUDED_FIELDS, many=True)

        # The query below is used to retrieve all products from the database
        products = products_schema.dump(Product.query.all())

        if not products:
            error_response['message'] = "No products found"
            return error_response, 404

        success_response['message'] = 'Products successfully fetched'
        success_response['data'] = {
            'products': products
        }
        return success_response, 200


# Endpoint to search for a product by the name of the product
@api.route('search/')
class SearchProductView(Resource):
    @api.expect(search_parser)
    def get(self):
        "search product"
        args = search_parser.parse_args()
        name = args.get('name')
        product_schema = ProductSchema(exclude=EXCLUDED_FIELDS, many=True)
        query = '%{}%'.format(args.get("name").strip("'"))

        # The query below is used to retrieve all products from the database where the name contains a specified substring
        product = Product.query.filter(Product.name.contains(query)).all()

        if not product:
            error_response['message'] = "This product does not exist"
            return error_response, 404

        success_response['message'] = "Product successfully fetched"
        success_response['data'] = product_schema.dump(product)
        return success_response, 200
