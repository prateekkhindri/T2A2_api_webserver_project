# Module for common validators

from werkzeug.exceptions import BadRequest


# Raises validation error
def raise_validation_error(message):

    error = BadRequest()
    error.data = {
        'status': 'error',
        'message': message
    }
    raise error


# Checks if the provided value is a positive integer
def is_positive_integer(value):

    if isinstance(value, int) and value > 0:
        return True
    else:
        return False


# Validates the user
class BaseValidators:

    @classmethod
    def base(cls, data: dict):
        for key, value in data.items():
            if not value or not value.strip():
                raise_validation_error(f'The {key} is required')
