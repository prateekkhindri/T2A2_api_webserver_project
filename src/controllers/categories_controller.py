from flask import request
from flask_restx import Namespace, Resource, fields
from src.utils.permission_required import permission_required
from src.utils.constants import EXCLUDED_FIELDS
from src.utils.token_required import token_required
from src.models.Category import Category
from src.schema.response.Category import CategorySchema
from src.utils import remove_space
from src.validators.category import CategoryValidators
from src.utils.responses import success_response, error_response

api = Namespace('category', description='Category Related Operations')
category_model = api.model('Category', {
    'name': fields.String(required=True, description='Category name'),
    'description': fields.String(required=False, description='Category description'),
})


# Endpoint to create a category - ONLY ADMIN CAN CREATE
@api.route('')
class CategoryView(Resource):

    @token_required
    @permission_required
    @api.expect(category_model)
    def post(self):

        request_data = request.get_json()
        CategoryValidators.validate(request_data)

        request_data = remove_space(request_data)
        request_data['name'] = request_data['name'].lower()
        new_category = Category(**request_data)
        new_category.save()

        category_schema = CategorySchema(exclude=EXCLUDED_FIELDS)
        category_data = category_schema.dump(new_category)

        success_response['message'] = 'Category successfully created'
        success_response['data'] = {
            'category': category_data
        }
        return success_response, 201

    # Endpoint to get all categories
    def get(self):
        """ Endpoint to get all categories """

        categories_schema = CategorySchema(exclude=EXCLUDED_FIELDS, many=True)

        # The query below is used to retrieve all categories from the database
        categories = categories_schema.dump(
            Category.query.all())

        if not categories:
            error_response['message'] = 'No categories found'
            return error_response, 404

        success_response['message'] = 'Categories successfully fetched'
        success_response['data'] = {
            'categories': categories
        }
        return success_response, 200


# Endpoint to get a single category
@api.route('<int:category_id>')
class SingleCategoryView(Resource):
    def get(self, category_id):
        category_schema = CategorySchema(exclude=EXCLUDED_FIELDS)
        category = category_schema.dump(Category.find_by_id(category_id))

        if not category:
            error_response['message'] = 'Category not found'
            return error_response, 404

        success_response['message'] = 'Category successfully fetched'
        success_response['data'] = {
            'category': category
        }
        return success_response, 200

    # Endpoint to update a category
    @token_required
    @permission_required
    @api.expect(category_model)
    def put(self, category_id):
        category_schema = CategorySchema(exclude=EXCLUDED_FIELDS)
        category = Category.find_by_id(category_id)

        if not category:
            error_response['message'] = 'Category not found'
            return error_response, 404

        request_data = request.get_json()
        CategoryValidators.validate(request_data, category_id=category_id)
        request_data = remove_space(request_data)
        request_data['name'] = request_data['name'].lower()

        category.update(request_data)

        updated_category = category_schema.dump(category)
        success_response['message'] = f'Category {updated_category["name"]} has been updated successfully'
        success_response['data'] = {
            'category': updated_category
        }
        return success_response, 200

    # Endpoint to delete a category
    @token_required
    @permission_required
    def delete(self, category_id):
        category_schema = CategorySchema(exclude=EXCLUDED_FIELDS)
        category = Category.find_by_id(category_id)

        if not category:
            error_response['message'] = 'Category not found'
            return error_response, 404

        category.delete()

        deleted_category = category_schema.dump(category)
        success_response['message'] = f'Category {deleted_category["name"]} has been deleted successfully'
        success_response['data'] = {
            'category': deleted_category
        }
        return success_response, 200
