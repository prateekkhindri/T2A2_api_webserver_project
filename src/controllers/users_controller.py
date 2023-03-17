from flask_restx import Resource, Namespace, reqparse
from src.utils.permission_required import permission_required, permission_seller
from src.utils import remove_space
from src.utils.constants import EXCLUDED_FIELDS
from src.utils.responses import success_response, error_response
from src.utils.token_required import token_required
from flask import request
from src.extension import session
from src.validators.product import ProductValidators
from src.schema.response.Product import ProductSchema
from src.models.Product import Product
from src.schema.response.User import UserSchema
from src.validators.user import UserValidators
from src.schema.request.User import user_fields, delete_fields
from src.models.User import User
from src.schema.request.Product import product_var, product_delete as product_del_variable, product_update


api = Namespace('user', description='User Related Operations')

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', required=False,
                         type=str, help="Enter the username")
user_parser.add_argument('email', required=False,
                         type=str, help="Enter the email address")
user_parser.add_argument('firstname', required=False,
                         type=str, help='Enter the first name')
user_parser.add_argument('lastname', required=False,
                         type=str, help='Enter the last name')

search_parser = reqparse.RequestParser()
search_parser.add_argument('name', required=False,
                           type=str, help='search by the product name')


user_model = api.model("user_model", user_fields)
delete_user = api.model("delete_user", delete_fields)
promote_admin = api.model("promote_admin", delete_fields)
product_model = api.model('Product', product_var)
product_delete = api.model('Product-Delete', product_del_variable)
product_update_model = api.model('Product-Update-Model', product_update)
user_exclude = ['created_at', 'updated_at', "password", "is_admin"]
admin_exclude = ['created_at', 'updated_at', "password"]


# Endpoint to GET a users profile (seller or buyer) by their username
@api.route('<string:username>/')
class UserView(Resource):
    def get(self, username):

        # The query below is used to retrieve a user's data from the database based on their username
        user = User.query.filter_by(username=username).first()

        if not user:
            error_response['message'] = "User does not exist"
            return error_response, 404

        user_schema = UserSchema(exclude=user_exclude)
        success_response["message"] = "User profile view"
        success_response['data'] = user_schema.dump(user)
        return success_response, 200

    # Endpoint to delete a user - ONLY ADMIN CAN ACTION
    @api.expect(delete_user)
    @token_required
    @permission_required
    def delete(self, username):
        request_data = request.get_json()

        user = User.find_by_id(request_data.get("id"))
        if not user:
            error_response['message'] = 'User does not exist'
            return error_response, 400

        if not user.username == username:
            error_response['message'] = "Incorrect username provided"
            return error_response, 400

        user.delete()

        user_schema = UserSchema(exclude=user_exclude)
        deleted_user = user_schema.dump(user)
        success_response['message'] = f'User {deleted_user["first_name"] + " " + deleted_user["last_name"]} has been deleted successfully'
        success_response['data'] = {
            'user': deleted_user
        }
        return success_response, 200

    # Endpoint for a user to update their profile
    @api.expect(user_model)
    @token_required
    def patch(self, username):
        data = request.get_json()
        UserValidators.validate_update(data)
        user_data = remove_space(data)
        user = User.find_by_id(session.current_user.get("id"))

        if not user:
            error_response['message'] = "User not found"
            return error_response, 404

        if not user.username == username:
            error_response['message'] = "Incorrect username provided"
            return error_response, 400

        user.update(user_data)
        user_schema = UserSchema(exclude=user_exclude)
        updated_user = user_schema.dump(user)
        success_response['message'] = f'{updated_user["first_name"] + " " + updated_user["last_name"]} your profile has been updated successfully'
        success_response['data'] = {
            'user': updated_user
        }
        return success_response, 200


# Endpoint to promote a user to admin - ONLY ADMIN CAN ACTION
@api.route("promote-admin/")
class PromoteAdminView(Resource):
    @api.expect(promote_admin)
    @token_required
    @permission_required
    def post(self):
        request_data = request.get_json()
        user = User.find_by_id(request_data.get("id"))
        if not user:
            error_response['message'] = "User does not exist"
            return error_response, 400
        user.update({"is_admin": True})

        user_schema = UserSchema(exclude=admin_exclude)
        updated_user = user_schema.dump(user)
        success_response['message'] = f'User {updated_user["first_name"] + " " + updated_user["last_name"]} has been promoted to admin'
        success_response['data'] = {
            'user': updated_user
        }
        return success_response, 200


# Endpoint to get all users from the database - ONLY ADMIN CAN ACTION
@api.route('all-users/')
class AllUserView(Resource):
    @token_required
    @permission_required
    def get(self):
        # The query below is used to retrieve all users data from the database
        user = User.query.all()

        if not user:
            error_response['message'] = "No users found"
            return error_response, 404

        user_schema = UserSchema(exclude=admin_exclude, many=True)
        return user_schema.dump(user)


# Endpoint to get all buyers - ONLY ADMIN CAN ACTION
@api.route('all-users/buyer/')
class AllUserBuyerView(Resource):
    @token_required
    @permission_required
    def get(self):

        # The query below is used to retrieve all non-seller and non-admin users from the database
        user = User.query.filter_by(is_seller=False, is_admin=False)

        if not user:
            error_response['message'] = "No users found"
            return error_response, 404

        user_schema = UserSchema(exclude=admin_exclude, many=True)
        return user_schema.dump(user)


# Endpoint to get all sellers - ONLY ADMIN CAN ACTION
@api.route('all-users/seller/')
class AllUserSellerView(Resource):
    @token_required
    @permission_required
    def get(self):

        # The query below is used to retrieve all users that are sellers from the database
        seller = User.query.filter_by(is_seller=True)

        if not seller:
            error_response['message'] = "No sellers found"
            return error_response, 404

        user_schema = UserSchema(exclude=admin_exclude, many=True)
        return user_schema.dump(seller)


# Endpoint to get all admins - ONLY ADMIN CAN ACTION
@api.route('all-users/admin/')
class AllUserAdminView(Resource):
    @token_required
    @permission_required
    def get(self):

        # The query below is used to retrieve all admin users from the database
        admin = User.query.filter_by(is_admin=True)

        if not admin:
            error_response['message'] = "No admin users found"
            return error_response, 404

        user_schema = UserSchema(exclude=admin_exclude, many=True)
        return user_schema.dump(admin)


# Endpoint to search for a user in the database - ONLY ADMIN CAN ACTION
@api.route('search/')
class UserSearch(Resource):
    @api.expect(user_parser)
    @token_required
    @permission_required
    def get(self):
        "search for a user in the database"
        args = user_parser.parse_args()
        user_schema = UserSchema(exclude=admin_exclude, many=True)
        query = '%{}%'.format(args.get("username").strip("'"))

        # The query below is used to search for a user in the database with their username. The filter method filters the username column of the Users table
        user = User.query.filter(User.username.contains(query)).all()

        if not user:
            error_response['message'] = "This user does not exist"
            return error_response, 404

        success_response['message'] = 'User successfully fetched'
        success_response['data'] = user_schema.dump(user)
        return success_response, 200


# Endpoint to get all products listed by a seller
@api.route('<string:username>/products/')
class SellerListedProducts(Resource):
    @token_required
    @permission_seller
    def get(self, username):
        user_id = session.current_user.get('id')

        # The query below is used to retrieve all products that belong to a specific seller, as identified by their seller_id
        product = Product.query.filter_by(seller_id=user_id)

        if not session.current_user.get('username') == username:
            error_response['message'] = 'The username provided is invalid'
            return error_response, 404

        if not product:
            error_response['message'] = 'No Product Found'
            return error_response, 404

        product_schema = ProductSchema(
            exclude=EXCLUDED_FIELDS, many=True)
        product_data = product_schema.dump(product)
        success_response['message'] = 'Products Successfully fetched'
        success_response['data'] = product_data
        return success_response, 200


# Endpoint to create a product by a seller
@api.route('<string:username>/product/')
class SellerListedSingleProduct(Resource):

    @api.expect(product_model)
    @token_required
    @permission_seller
    def post(self, username):
        user_id = session.current_user.get("id")

        if not session.current_user.get('username') == username:
            error_response['message'] = 'Incorrect username provided'
            return error_response, 401

        request_data = request.get_json()
        ProductValidators.validate(request_data)

        request_data = remove_space(request_data)
        request_data['seller_id'] = user_id
        request_data['name'] = request_data['name'].lower()
        new_product = Product(**request_data)
        new_product.save()

        product_schema = ProductSchema(exclude=EXCLUDED_FIELDS)
        product_data = product_schema.dump(new_product)

        success_response['message'] = 'Product successfully created'
        success_response['data'] = {
            'product': product_data
        }
        return success_response, 201

    # Endpoint to delete a product by a seller
    @api.expect(product_delete)
    @token_required
    @permission_seller
    def delete(self, username):
        request_data = request.get_json()
        user_id = session.current_user.get('id')

        if not session.current_user.get('username') == username:
            error_response['message'] = 'Incorrect username provided'
            return error_response, 401

        product = Product.find_by_id(request_data.get("id"))

        if not product:
            error_response['message'] = 'This product does not exist'
            return error_response, 400

        if product.seller_id != user_id:
            error_response['message'] = 'You are not allowed to delete this product'
            return error_response, 404
        product.delete()

        product_schema = ProductSchema(exclude=EXCLUDED_FIELDS)
        deleted_product = product_schema.dump(product)
        success_response['message'] = f'Product {deleted_product["name"]} has been deleted successfully'
        success_response['data'] = {
            'product': deleted_product
        }
        return success_response, 200

    # Endpoint to update a product by a seller
    @api.expect(product_update_model)
    @token_required
    @permission_seller
    def patch(self, username):
        user = session.current_user

        request_data = request.get_json()
        id = request_data['id']
        del request_data['id']
        ProductValidators.validate(request_data)
        request_data = remove_space(request_data)
        request_data['name'] = request_data['name'].lower()
        updated_product = Product.find_by_id(id)

        if not session.current_user.get('username') == username:
            error_response['message'] = 'Incorrect username provided'
            return error_response, 401

        if not updated_product:
            error_response['message'] = 'This product does not exist'
            return error_response, 400

        if user.get('id') != updated_product.seller_id:
            error_response['message'] = 'You are not allowed to update this product'
            return error_response, 404

        updated_product.update(request_data)
        product_schema = ProductSchema(exclude=EXCLUDED_FIELDS)
        product_data = product_schema.dump(updated_product)

        success_response['message'] = f'Product {product_data["name"]} has been updated successfully'
        success_response['data'] = {
            'product': product_data
        }
        return success_response, 200
