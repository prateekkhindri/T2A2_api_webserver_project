# Module for permission validation

from functools import wraps
from flask import request
from src.models.User import User
from src.schema.response.User import UserSchema
from src.utils.responses import error_response


# Validates if the user is allowed to perform a certain action
def permission_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        decoded_token = request.decoded_token
        current_user = User.find_by_id(decoded_token['user']['id'])
        user_schema = UserSchema()
        user_data = user_schema.dump(current_user)

        if not current_user:
            error_response['message'] = 'Token is not valid'
            return error_response, 401

        if not user_data['is_admin']:
            message = 'Permission denied. You are not authorized to perform this action'
            error_response['message'] = message
            return error_response, 403

        return f(*args, **kwargs)
    return decorated


# Validates if the user is allowed to perform a certain action
def permission_seller(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        decoded_token = request.decoded_token
        current_user = User.find_by_id(decoded_token['user']['id'])
        user_schema = UserSchema()
        user_data = user_schema.dump(current_user)

        if not current_user:
            error_response['message'] = 'Token is not valid'
            return error_response, 401

        if not user_data['is_seller']:
            message = 'Permission denied. You are not a seller to perform this task'
            error_response['message'] = message
            return error_response, 403

        return f(*args, **kwargs)
    return decorated
