from flask import request
from flask_restful import Resource

from models.order import OrderModel
from models.user import UserModel
from models.cart import CartModel

class Order(Resource):
    @classmethod
    def get(cls, order_id):
        order = OrderModel.find_by_id(order_id)

        if not order:
            return {'message': "Order with id '{}' doesn't exist".format(order_id)}, 404

        return order.to_json()


class OrderCreate(Resource):
    def post(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "This user doesn't exist"}, 404

        user_cart = CartModel.find_by_user_id(user_id)
        print()
        if len(user_cart.products.all()) == 0:
            return {'message': "Cart of this user is empty"}, 404

        order = OrderModel(user_id, user_cart.products)
        order.save_to_db()

        user_cart.delete_all_from_cart()

        return order.to_json()

