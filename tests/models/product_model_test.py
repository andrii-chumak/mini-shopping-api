from pytest import fixture
from flask_sqlalchemy import SQLAlchemy
from tests.fixtures import app, db
from models.product import ProductModel


@fixture
def product() -> ProductModel:
    return ProductModel(name="Test", price=12.9)


def test_product_create(product: ProductModel):
    assert product


def test_product_retrieve(product: ProductModel, db: SQLAlchemy):
    db.session.add(product)
    db.session.commit()
    product_res = ProductModel.query.first()
    assert product.__dict__ == product_res.__dict__
