from flask import request
from flask_restful import Resource

from models.product import ProductModel


class Product(Resource):
    @classmethod
    def get(cls, product_id):
        user = ProductModel.find_by_id(product_id)

        if not user:
            return {'message': "Product with id '{}' doesn't exist".format(product_id)}, 404

        return user.to_json()


class ProductCreate(Resource):
    def post(self):
        data = request.get_json()

        product = ProductModel(**data)
        ProductModel.save_to_db(product)

        return {'message': 'Product successfully added'}
