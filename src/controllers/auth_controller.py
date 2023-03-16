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


api = Namespace('auth', description='auth related operations')

login_model = api.model("login-model", login_schema)
reset_model = api.model("reset-model", reset_schema)
signup_model = api.model("signup", normal_user)


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
