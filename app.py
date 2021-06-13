from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import User, UserRegister
from resources.order import Order, OrderCreate
from resources.product import Product, ProductCreate, ProductList
from resources.cart import Cart, CartTotal

from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'


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


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
