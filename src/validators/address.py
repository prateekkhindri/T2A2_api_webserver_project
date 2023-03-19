from src.validators import raise_validation_error
import re


# Address validators class
class AddressValidators:

    # Validates the address data
    @classmethod
    def validate(cls, data: dict):
        required_fields = ['street_address', 'suburb', 'state', 'postcode']

        regex = {
            'street_address': r'^\d{1,5}\s[a-zA-Z0-9\s\.,-]+$',
            'suburb': r'^[a-zA-Z\s]{1,40}$',
            'state': r'^(VIC|NSW|QLD|ACT|SA|WA|NT|TAS)$',
            'postcode': r'^\d{4}$'
        }

        for field in required_fields:
            if not data.get(field) or not data.get(field).strip():
                raise_validation_error(f'The {field} is required')
            if not re.match(regex[field], data.get(field).strip()):
                raise_validation_error(f'The {field} is not valid')
