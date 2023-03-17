from flask import request
from flask_restx import Namespace, Resource
from src.models.Address import Address
from src.schema.response.Address import AddressSchema
from src.utils.constants import EXCLUDED_FIELDS
from src.schema.request.Address import address_create, address_update
from src.utils.token_required import token_required
from src.utils import remove_space
from src.validators.address import AddressValidators
from src.utils.responses import success_response, error_response
from src.extension import session


api = Namespace('address', description='address related operations')
address_create_model = api.model("address-create-model", address_create)
address_update_model = api.model("address-update-model", address_update)


# Endpoint to get all user addresses from the database
@api.route("")
class AddressView(Resource):
    @token_required
    def get(self):
        user_id = session.current_user.get('id')

        # This query retrieves all the addresses where the user_id is equal to the current user's id
        # It returns a list of Address objects
        address = Address.query.filter_by(user_id=user_id)

        if not address:
            error_response['message'] = 'No address found'
            return error_response, 404

        address_schema = AddressSchema(exclude=EXCLUDED_FIELDS, many=True)
        address_data = address_schema.dump(address)
        success_response['message'] = 'Address successfully retrieved'
        success_response['data'] = {
            'address': address_data
        }
        return success_response, 200

    # Endpoint to create a new address
    @api.expect(address_create_model)
    @token_required
    def post(self):
        "create address "
        request_data = request.get_json()
        AddressValidators.validate(request_data)
        request_data = remove_space(request_data)
        user_id = session.current_user.get("id")
        request_data['user_id'] = user_id
        new_address = Address(**request_data)
        new_address.save()
        address_schema = AddressSchema(exclude=EXCLUDED_FIELDS)
        address_data = address_schema.dump(new_address)

        success_response['message'] = 'Address has been created successfully'
        success_response['data'] = {
            'address': address_data
        }
        return success_response, 201


# Endpoint to delete an address sending the address id
@api.route('<int:address_id>/')
class AddressSingleView(Resource):
    @token_required
    def delete(self, address_id):
        "delete address token required "
        user_id = session.current_user.get('id')

        # This query is intended to retrieve a single address object with the given id and user_id values, which can be used to check if an address exists for a given user
        address = Address.query.filter_by(
            id=address_id, user_id=user_id).first()

        address_schema = AddressSchema(exclude=EXCLUDED_FIELDS)
        if address:
            address.delete()
            deleted_address = address_schema.dump(address)
            success_response['message'] = f'Address {deleted_address["id"]} has been deleted successfully'
            success_response['data'] = {
                'address': deleted_address
            }
            return success_response, 200
        else:
            error_response['message'] = 'Address not found'
            return error_response, 404

    # Endpoint to update an address sending the address id
    @api.expect(address_update_model)
    @token_required
    def put(self, address_id):
        user_id = session.current_user.get('id')

        # This query is intended to retrieve a single address object with the given id and user_id values, which can be used to check if an address exists for a given user
        address = Address.query.filter_by(
            id=address_id, user_id=user_id).first()
        if address:
            request_data = request.get_json()
            AddressValidators.validate(request_data, is_update=True)
            request_data = remove_space(request_data)
            address.update(request_data)
            address_schema = AddressSchema(exclude=EXCLUDED_FIELDS)
            updated_address = address_schema.dump(address)
            success_response['message'] = f'Address {updated_address["id"]} has been updated successfully'
            success_response['data'] = {
                'address': updated_address
            }
            return success_response, 200
        else:
            error_response['message'] = 'Address not found'
            return error_response, 404

    # Endpoint to get a single address sending the address id
    @token_required
    def get(self, address_id):
        user_id = session.current_user.get('id')
        address_schema = AddressSchema(exclude=EXCLUDED_FIELDS)

        # This query is intended to retrieve a single address object with the given id and user_id values, which can be used to check if an address exists for a given user
        address = Address.query.filter_by(
            id=address_id, user_id=user_id).first()

        if not address:
            error_response['message'] = 'Address not found'
            return error_response, 404

        address_data = address_schema.dump(address)
        success_response['message'] = f'Address {address_data["id"]} successfully retrieved'
        success_response['data'] = {
            'address': address_data
        }
        return success_response, 200
