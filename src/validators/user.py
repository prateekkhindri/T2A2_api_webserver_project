from src.validators import raise_validation_error
from src.models.User import User
import re


class UserValidators:

    # Checks if the provided email is valid
    @classmethod
    def validate_email(cls, email):
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email.strip()):
            raise_validation_error('The email provided is not valid')

        if User.query.filter(User.email == email.strip()).first():
            raise_validation_error('The email provided already exists')

    # Validate the password
    @classmethod
    def validate_password(cls, password):
        if len(password) < 8:
            raise_validation_error(
                'The password must be at least 8 characters')

        if not any(char.isupper() for char in password):
            raise_validation_error(
                'The password must have at least one uppercase letter')

        if not any(char.islower() for char in password):
            raise_validation_error(
                'The password must have at least one lowercase letter')

        if not any(char.isdigit() for char in password):
            raise_validation_error(
                'The password must have at least one digit')

    @classmethod
    def validate_update(cls, data: dict):
        for key, value in data.items():
            if not value or not value.strip():
                raise_validation_error(f'The {key} is required')

    @classmethod
    def validate(cls, data: dict):
        cls.validate_update(data)
        cls.validate_email(data.get('email'))
        cls.validate_password(data.get('password'))
