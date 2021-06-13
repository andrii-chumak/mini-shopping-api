from pytest import fixture
from flask_sqlalchemy import SQLAlchemy
from tests.fixtures import app, db
from models.cart import CartModel


@fixture
def cart() -> CartModel:
    return CartModel(user_id=1)


def test_cart_create(cart: CartModel):
    assert cart


def test_cart_retrieve(cart: CartModel, db: SQLAlchemy):
    db.session.add(cart)
    db.session.commit()
    cart_res = CartModel.query.first()
    assert cart.__dict__ == cart_res.__dict__
