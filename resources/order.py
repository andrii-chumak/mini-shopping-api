from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.order import OrderModel
from models.cart import CartModel

from utils.cart_calculations import calculate_total


class Order(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('status',
                        type=str,
                        required=True,
                        help="You need write status to change it"
                        )

    @jwt_required()
    def get(self, order_id):
        order = OrderModel.find_by_id(order_id)

        if not order:
            return {'message': "Order with id '{}' doesn't exist".format(order_id)}, 404

        return order.to_json()

    @jwt_required()
    def post(self, order_id):
        data = Order.parser.parse_args()
        order = OrderModel.find_by_id(order_id)

        if not order:
            return {'message': "Order with id '{}' doesn't exist".format(order_id)}, 404

        order.set_status(**data)
        return order.to_json()


class OrderCreate(Resource):
    @jwt_required()
    def post(self):
        user = current_identity
        user_cart = CartModel.find_by_user_id(user.id)
        if len(user_cart.products.all()) == 0:
            return {'message': "Cart of this user is empty"}, 404

        order = OrderModel(user.id, user_cart.products, calculate_total(user_cart))
        order.save_to_db()

        for product in user_cart.products:
            quantity = user_cart.get_quantity_by_product_id(product.id)
            free_products = user_cart.get_number_free_products(product.id)

            order.set_quantity_by_product_id(product.id, quantity)
            order.set_number_free_products(product.id, free_products)

        user_cart.delete_all_from_cart()

        return order.to_json()

