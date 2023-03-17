from flask import request
from flask_restx import Namespace, Resource
from src.utils.token_required import logout_user, token_required
from src.schema.request.Auth import login_schema, reset_schema, normal_user
from src.utils import remove_space
from src.utils.generate_token import verify_token, generate_auth_token
from src.schema.response.User import UserSchema
from src.validators.user import UserValidators
from src.models.User import User
from src.utils.responses import error_response, success_response
from src.extension import bcrypt
from sqlalchemy.exc import IntegrityError


api = Namespace('auth', description='Auth Related Operations')

login_model = api.model("login-model", login_schema)
reset_model = api.model("reset-model", reset_schema)
signup_model = api.model("signup", normal_user)


# Buyer signup endpoint
@api.route("signup/buyer/")
class SignupBuyerView(Resource):
    @api.expect(signup_model)
    def post(self):
        try:
            data = request.get_json()
            UserValidators.validate(data)
            data = remove_space(data)
            data['password'] = bcrypt.generate_password_hash(
                data.get("password")).decode('utf-8')
            new_user = User(**data)
            new_user.save()
            user_schema = UserSchema()
            user_data = user_schema.dump(new_user)

            return {
                'status': 'success',
                'message': 'User account created successfully',
            }, 201

        except IntegrityError:
            return {"message": "This email already exists"}, 409


# Seller signup endpoint
@api.route("signup/seller/")
class SignupSellerView(Resource):
    @api.expect(signup_model)
    def post(self):
        try:
            data = request.get_json()
            UserValidators.validate(data)
            data = remove_space(data)
            data['password'] = bcrypt.generate_password_hash(
                data.get("password")).decode('utf-8')
            new_user = User(**data)
            new_user.save_seller()
            user_schema = UserSchema()
            user_data = user_schema.dump(new_user)

            return {
                'status': 'success',
                'message': 'Seller account created successfully',
            }, 201
        except IntegrityError:
            return {"message": "This email already exists"}, 409


# User Login endpoint
@api.route("login/")
class LoginView(Resource):
    @api.expect(login_model)
    def post(self):
        request_data = request.get_json()
        email = request_data.get("email")
        password = request_data.get("password")

        # The query below is used to retrieve a user's data from the database based on their email address.
        user = User.query.filter_by(email=email).first()
        user_schema = UserSchema()

        if user:
            user_data = user_schema.dump(user)
            if bcrypt.check_password_hash(user_data.get("password"), password):
                token = generate_auth_token(user_data)
                user_schema = UserSchema(exclude=['password'])
                logged_in_user = user_schema.dump(user)
                success_response['message'] = f'Login successful, welcome {logged_in_user["first_name"] + " " + logged_in_user["last_name"]}'
                success_response['data'] = {
                    'user': user.email,
                    'token': token
                }
                return success_response, 200
            else:
                return error_response, 203
        else:
            error_response['message'] = "This account does not exist, please signup"
            return error_response, 404


# Password reset endpoint
@api.route("reset-password/<string:token>/", endpoint="recovery")
class PasswordResetView(Resource):
    @api.expect(reset_model)
    def patch(self, token):
        user = verify_token(token)
        if not user:
            error_response['message'] = 'Password reset token is invalid'
            return error_response, 400
        request_data = request.get_json()
        UserValidators.validate_password(request_data.get("password"))
        request_data = remove_space(request_data)
        password = bcrypt.generate_password_hash(
            request_data.get("password")).decode('utf-8')
        user.update({'password': password})
        return {
            'status': 'success',
            'message': f'{user.firstname} {user.lastname}, your password has been updated successfully'
        }, 200


# User logout endpoint
@api.route("logout/")
class LogoutView(Resource):
    @token_required
    def get(self):
        logout_user()
        return {
            'message': 'You have successfully logged out'
        }, 200
