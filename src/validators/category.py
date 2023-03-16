# Module for category validators

from flask import request
from src.models.Category import Category
from . import raise_validation_error


# Category validators class
class CategoryValidators:

    # Checks if the provided name doesn't exist
    @classmethod
    def validate_name(cls, name, category_id=None):
        category = Category.query.filter(
            Category.name == name.lower().strip()).first()

        if category:
            if request.method == 'PUT':
                if category_id != category.id:
                    raise_validation_error(
                        'The category name provided already exists')
            else:
                raise_validation_error(
                    'The category name provided already exists')

    # Validates the category
    @classmethod
    def validate(cls, data: dict, category_id=None):

        name = data.get('name')
        parent_id = data.get('parent_id')
        if not name or not name.strip():
            raise_validation_error('The category name is required')

        cls.validate_name(name, category_id)

        if parent_id:
            category = Category.find_by_id(parent_id)
            if not category:
                raise_validation_error(
                    'The parent category provided doesn\'t exist')
