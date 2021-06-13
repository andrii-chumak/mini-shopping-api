from flask_restful import Resource, reqparse

from models.product import ProductModel


class Product(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('price', type=float)

    @classmethod
    def get(cls, product_id):
        product = ProductModel.find_by_id(product_id)

        if product:
            return product.to_json()
        return {'message': "Product with id '{}' doesn't exist".format(product_id)}, 404

    def put(self, product_id):
        data = Product.parser.parse_args()
        product = ProductModel.find_by_id(product_id)

        if product is None:
            if data['name'] and data['price']:
                product = ProductModel(**data)
                product.save_to_db()
            else:
                return {'message': "This product doesn't exist, you should enter all data to create one"}, 404
        else:
            product.name = data['name'] if data['name'] else product.name
            product.price = data['price'] if data['price'] else product.price

        product.save_to_db()

        return product.to_json()

    def delete(self, product_id):
        product = ProductModel.find_by_id(product_id)
        if product:
            product.delete_from_db()

            return {'message': "Product deleted"}
        else:
            return {'message': "Product doesn't exist"}, 404


class ProductCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="The product should have a name"
                        )

    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="The product should have a price"
                        )

    def post(self):
        data = ProductCreate.parser.parse_args()

        if data['price'] <= 0:
            return {'message': 'Product should have price greater than zero'}, 400

        product = ProductModel(**data)
        product.save_to_db()

        return {'message': 'Product successfully added'}, 201


class ProductList(Resource):
    @classmethod
    def get(cls):
        return {'products': [product.to_json() for product in ProductModel.find_all()]}
