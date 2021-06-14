from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.cart import CartModel
from models.product import ProductModel

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

    @jwt_required()
    def get(self):
        """
            Call this query to get user's cart
            ---
            headers:
              - Authorization: JWT {{jwt_token}}
            responses:
              200:
                id:         id of cart in db
                user_id:    id of cart owner
                products:   list of products in the cart
              401:
                description: "Signature verification failed"
                error:       "Invalid token"
                status_code: 401

        """
        user = current_identity

        cart = CartModel.find_by_user_id(user.id)
        return cart.to_json()

    @jwt_required()
    def post(self):
        """
            Call this query to get add product to the user's cart
            ---
            headers:
              - Authorization: JWT {{jwt_token}}
              - Content-Type: application/json
            json:
              - product_id: int
            responses:
              200:
                id:         id of cart in db
                user_id:    id of cart owner
                products:   list of products in the cart
              401:
                description: "Signature verification failed"
                error:       "Invalid token"
                status_code: 401
              404:
                "message": "This product doesn't exist"
        """
        data = Cart.parser.parse_args()
        user = current_identity

        cart = CartModel.find_by_user_id(user.id)

        product = ProductModel.find_by_id(data['product_id'])
        if not product:
            return {'message': "This product doesn't exist"}, 404

        cart.add_product(product)
        result, message = check_preconditions(cart)

        if result:
            return cart.to_json()

        cart.remove_product(product)
        return {'message': message}

    @jwt_required()
    def delete(self):
        user = current_identity
        cart = CartModel.find_by_user_id(user.id)
        cart.delete_all_from_cart()

        return {'message': "The cart was cleaned"}, 404


class CartTotal(Resource):
    @jwt_required()
    def get(self):
        """
            Call this query to get add product to the user's cart
            ---
            headers:
              - Authorization: JWT {{jwt_token}}
            responses:
              200:
                id:         id of cart in db
                user_id:    id of cart owner
                products:   list of products in the cart
                subtotal:   float
                total:      float
              401:
                description: "Signature verification failed"
                error:       "Invalid token"
                status_code: 401
        """
        user = current_identity
        cart = CartModel.find_by_user_id(user.id)
        products = [product.to_json() for product in cart.products.all()]
        for product in products:
            product['quantity'] = cart.get_quantity_by_product_id(product['id'])
            product['free'] = cart.get_number_free_products(product['id'])

        return {
            'products': products,
            'subtotal': calculate_subtotal(cart),
            'total': calculate_total(cart)
        }
