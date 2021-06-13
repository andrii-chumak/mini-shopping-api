from pytest import fixture
from flask_sqlalchemy import SQLAlchemy
from tests.fixtures import app, db
from models.order import OrderModel, OrderStatus


@fixture
def order() -> OrderModel:
    return OrderModel(user_id=1, products=[], total=12.9)


def test_order_create(order: OrderModel):
    assert order


def test_order_retrieve(order: OrderModel, db: SQLAlchemy):
    db.session.add(order)
    db.session.commit()
    order_res = OrderModel.query.first()
    assert order.__dict__ == order_res.__dict__
    assert order.status == OrderStatus.created
