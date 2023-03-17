from src.validators import raise_validation_error
from src.models.Product import Product


class CartValidators:

    # Cart item validation
    @classmethod
    def validate_item(cls, data: dict):
        """ Validates the cart item """

        product_id = data.get('product_id')
        quantity = data.get('quantity')

        cls.validate_product_id(product_id)
        cls.validate_quantity(quantity)

        product = Product.find_by_id(product_id)
        product_quantity = product.quantity
        user_needed_quantity = quantity

        if product_quantity - user_needed_quantity < 0:
            raise_validation_error('The product is not available')
