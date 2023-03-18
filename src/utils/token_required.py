# Module for auth token validation

from os import environ
from functools import wraps
import jwt
from flask import request
from src.utils.responses import error_response
from src.extension import session
BlOCK_LIST = []


def logout_user():
    token = request.headers['Authorization']
    BlOCK_LIST.append(token)


# Validates token from the user
def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

            if request.path == '/auth/logout/':
                decoded_token = None

            elif token in BlOCK_LIST:
                error_response['message'] = 'Token is expired'
                return error_response, 401

        if not token:
            message = 'No authorization token provided'
            error_response['message'] = message
            return error_response, 401

        try:
            decoded_token = jwt.decode(token, environ.get(
                'SECRET_KEY'), algorithms=['HS256'])

            session.current_user = decoded_token.get("user")
            session.token = token

        except:
            error_response['message'] = 'The provided authorization token is invalid'
            return error_response, 401

        setattr(request, 'decoded_token', decoded_token)
        return f(*args, **kwargs)
    return decorated
