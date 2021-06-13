from flask_restful import Resource, reqparse

from models.cart import CartModel
from models.product import ProductModel
from models.user import UserModel

from utils.cart_calculations import (
    check_preconditions,
    calculate_subtotal,
    calculate_total,
)


class Cart(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_id',
                        type=int,
                        required=True,
                        help="To add the product to the cart you should provide product_id."
                        )

    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "This user doesn't exist"}, 404

        cart = CartModel.find_by_user_id(user_id)
        return cart.to_json()

    def post(self, user_id):
        data = Cart.parser.parse_args()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "This user doesn't exist"}, 404

        cart = CartModel.find_by_user_id(user_id)

        product = ProductModel.find_by_id(data['product_id'])
        if not product:
            return {'message': "This product doesn't exist"}

        cart.add_product(product)
        result, message = check_preconditions(cart)

        if result:
            return cart.to_json()

        cart.remove_product(product)
        return {'message': message}


    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "This user doesn't exist"}, 404

        cart = CartModel.find_by_user_id(user_id)
        cart.delete_all_from_cart()

        return {'message': "The cart was cleaned"}, 404


class CartTotal(Resource):
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "This user doesn't exist"}, 404

        cart = CartModel.find_by_user_id(user_id)
        products = [product.to_json() for product in cart.products.all()]
        for product in products:
            product['quantity'] = cart.get_quantity_by_product_id(product['id'])
            product['free'] = cart.get_number_free_products(product['id'])

        return {
            'products': products,
            'subtotal': calculate_subtotal(cart),
            'total': calculate_total(cart)
        }
