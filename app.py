import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import User, UserRegister
from resources.order import Order, OrderCreate
from resources.product import Product, ProductCreate, ProductList
from resources.cart import Cart, CartTotal

from database import db


def create_app(env=None):
    app = Flask(__name__)
    if env == 'test':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    else:
        uri = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)

        app.config['SQLALCHEMY_DATABASE_URI'] = uri

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = ''

    api = Api(app)
    jwt = JWT(app, authenticate, identity)

    api.add_resource(User, '/user/<int:user_id>')
    api.add_resource(UserRegister, '/register')
    api.add_resource(Order, '/order/<int:order_id>')
    api.add_resource(OrderCreate, '/create-order')
    api.add_resource(Product, '/product/<int:product_id>')
    api.add_resource(ProductCreate, '/product-create')
    api.add_resource(ProductList, '/products')
    api.add_resource(Cart, '/cart')
    api.add_resource(CartTotal, '/cart-total')

    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, debug=False)
