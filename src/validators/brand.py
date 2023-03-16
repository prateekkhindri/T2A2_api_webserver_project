# Module for brand validators

from flask import request
from src.models.Brand import Brand
from . import raise_validation_error


# Brand validators class
class BrandValidators:

    # Checks if the provided name doesn't exist
    @classmethod
    def validate_name(cls, name, brand_id=None):

        brand = Brand.query.filter(Brand.name == name.lower().strip()).first()

        if brand:
            if request.method == 'PUT':
                if brand_id != brand.id:
                    raise_validation_error(
                        'The brand name provided already exists')
            else:
                raise_validation_error(
                    'The brand name provided already exists')

    # Validates the brand
    @classmethod
    def validate(cls, data: dict, brand_id=None):

        name = data.get('name')

        if not name or not name.strip():
            raise_validation_error('The brand name is required')

        cls.validate_name(name, brand_id)
