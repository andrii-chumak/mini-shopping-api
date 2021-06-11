from flask import request
from flask_restful import Resource

from models.order import OrderModel


class Order(Resource):
    @classmethod
    def get(cls, order_id):
        order = OrderModel.find_by_id(order_id)

        if not order:
            return {'message': "Order with id '{}' doesn't exist".format(order_id)}, 404

        return order.to_json()

    def post(self):
        pass
