import datetime
from os import environ
import jwt
from src.models.User import User


def verify_token(token):
    try:
        user_id = jwt.decode(token, key=environ.get(
            "SECRET_KEY"), algorithms=['HS256']).get("user").get("id")
    except Exception:
        return None
    return User.find_by_id(user_id)


# Generates the authentication token and returns it
def generate_auth_token(user: dict):

    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'user': user
    }
    token = jwt.encode(
        payload,
        environ.get('SECRET_KEY'),
        algorithm='HS256'
    )
    return token
