from flask_restful import Resource, reqparse

from models.cart import CartModel
from models.product import ProductModel
from models.user import UserModel


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
        if product:
            cart.add_product(product)
            return cart.to_json()

        return {'message': "This product doesn't exist"}

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "This user doesn't exist"}, 404

        cart = CartModel.find_by_user_id(user_id)
        cart.delete_all_from_cart()

        return {'message': "The cart was cleaned"}, 404
