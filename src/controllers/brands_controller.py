from flask import request
from flask_restx import Namespace, Resource, fields
from src.utils.permission_required import permission_required, permission_seller
from src.utils.token_required import token_required
from src.schema.response.Brand import BrandSchema
from src.utils import remove_space
from src.validators.brand import BrandValidators
from src.utils.constants import EXCLUDED_FIELDS
from src.models.Brand import Brand
from src.utils.responses import success_response, error_response

api = Namespace('brand', description='Brand Related Operations')

brand_model = api.model('Brand', {
    'name': fields.String(required=True, description='Brand name'),
    'description': fields.String(required=False, description='Brand description')
})


# Endpoint to create the brand you have to be an admin
@api.route("")
class BrandView(Resource):
    @token_required
    @permission_required
    @api.expect(brand_model)
    def post(self):

        request_data = request.get_json()
        BrandValidators.validate(request_data)

        request_data = remove_space(request_data)
        request_data['name'] = request_data['name'].lower()

        new_brand = Brand(**request_data)
        new_brand.save()

        brand_schema = BrandSchema(exclude=EXCLUDED_FIELDS)
        brand_data = brand_schema.dump(new_brand)

        success_response['message'] = 'Brand has been created successfully'
        success_response['data'] = {
            'brand': brand_data
        }
        return success_response, 201

    # Endpoint to get all brands
    def get(self):
        brands_schema = BrandSchema(exclude=EXCLUDED_FIELDS, many=True)

        # The query below is used to retrieve all brands from the database
        brands = brands_schema.dump(
            Brand.query.all())

        if not brands:
            error_response['message'] = 'No brands found'
            return error_response, 404

        success_response['message'] = 'Brands successfully fetched'
        success_response['data'] = {
            'brands': brands
        }

        return success_response, 200


# Endpoint to get a single brand
@api.route('<int:brand_id>')
class SingleBrandResource(Resource):
    def get(self, brand_id):

        brand_schema = BrandSchema(exclude=EXCLUDED_FIELDS)
        brand = brand_schema.dump(Brand.find_by_id(brand_id))

        if not brand:
            error_response['message'] = 'Brand not found'
            return error_response, 404

        success_response['message'] = f'Brand {brand["name"]} successfully fetched'
        success_response['data'] = {
            'brand': brand
        }

        return success_response, 200

    # Update the brand by id - Only admin can action
    @token_required
    @permission_required
    @api.expect(brand_model)
    def put(self, brand_id):

        brand_schema = BrandSchema(exclude=EXCLUDED_FIELDS)
        brand = Brand.find_by_id(brand_id)

        if not brand:
            error_response['message'] = 'Brand not found'
            return error_response, 404

        request_data = request.get_json()
        BrandValidators.validate(request_data, brand_id=brand_id)
        request_data = remove_space(request_data)
        request_data['name'] = request_data['name'].lower()

        brand.update(request_data)
        updated_brand = brand_schema.dump(brand)

        success_response['message'] = f'Brand {updated_brand["name"]} has been updated successfully'
        success_response['data'] = {
            'brand': updated_brand
        }

        return success_response, 200

    # Endpoint to delete a brand - Only admin can action
    @token_required
    @permission_required
    def delete(self, brand_id):
        """" Endpoint to delete a brand """

        brand_schema = BrandSchema(exclude=EXCLUDED_FIELDS)
        brand = Brand.find_by_id(brand_id)

        if not brand:
            error_response['message'] = 'Brand not found'
            return error_response, 404

        brand.delete()

        deleted_brand = brand_schema.dump(brand)
        success_response['message'] = f'Brand {deleted_brand["name"]} has been deleted successfully'
        success_response['data'] = {
            'brand': deleted_brand
        }

        return success_response, 200
