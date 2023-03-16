# Module for product validators

import numbers
from flask import request
from src.models.Product import Product
from src.models.Category import Category
from src.models.Brand import Brand
from . import raise_validation_error, is_positive_integer


# Product validators class
class ProductValidators:

    # Checks if the provided name doesn't exist
    @classmethod
    def validate_name(cls, name, product_id=None):
        if not name or not name.strip():
            raise_validation_error(
                'The product name is required')

        product = Product.query.filter(
            Product.name == name.lower().strip()).first()

        if product:
            if request.method == 'PUT':
                if product_id != product.id:
                    raise_validation_error(
                        'The product name provided already exists')
            else:
                raise_validation_error(
                    'The product name provided already exists')

    # Checks if the provided category ID is valid
    @classmethod
    def validate_category(cls, category_id):
        if not category_id:
            raise_validation_error(
                'The category ID is required')

        if not is_positive_integer(category_id):
            raise_validation_error(
                'The category ID should be a positive integer')

        if not Category.find_by_id(category_id):
            raise_validation_error('The category ID provided doesn\'t exist')

    # Checks if the provided brand ID is valid
    @classmethod
    def validate_brand(cls, brand_id):
        if brand_id is not None:
            if not is_positive_integer(brand_id):
                raise_validation_error(
                    'The brand ID should be a positive integer')

            if not Brand.find_by_id(brand_id):
                raise_validation_error(
                    'The brand ID provided doesn\'t exist')

    # Validates the product
    @classmethod
    def validate(cls, data: dict, product_id=None):

        name = data.get('name')
        category_id = data.get('category_id')
        brand_id = data.get('brand_id')
        price = data.get('price')
        quantity = data.get('quantity')

        cls.validate_name(name, product_id)
        cls.validate_category(category_id)
        cls.validate_brand(brand_id)

        if price is None:
            raise_validation_error('The price is required')

        if not isinstance(price, numbers.Number) or price < 0:
            raise_validation_error('The price must be a positive number')

        if quantity is None:
            raise_validation_error('The quantity is required')

        if not is_positive_integer(quantity):
            raise_validation_error('The quantity must be a positive integer')
