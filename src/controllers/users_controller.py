from flask_restx import Resource, Namespace, reqparse
from src.utils.permission_required import permission_required, permission_seller
from src.utils import remove_space
from src.utils.constants import EXCLUDED_FIELDS
from src.utils.responses import success_response, error_response
from src.utils.token_required import token_required
from flask import request
from src.extension import session
from src.schema.response.User import UserSchema
from src.validators.user import UserValidators
from src.schema.request.User import user_fields, delete_fields
from src.models.User import User


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
