from flask_sqlalchemy import SQLAlchemy
from flask.testing import FlaskClient
from tests.fixtures import app, db, client
from models.product import ProductModel
from resources.product import Product, ProductList, ProductCreate


def test_get(db: SQLAlchemy):
    product = ProductModel(name="Test", price=5.25)

    db.session.add(product)
    db.session.commit()

    result = Product.get(1)

    assert result['name'] == product.name
    assert result['price'] == product.price


def test_put(client: FlaskClient):
    payload = dict(name='Test', price=7.8)
    result = client.put(
        '/product/1',
        json=payload
    ).get_json()

    assert result['name'] == payload['name']
    assert result['price'] == payload['price']


def test_delete(db: SQLAlchemy, client: FlaskClient):
    product = ProductModel(name="Test", price=5.25)
    db.session.add(product)
    db.session.commit()

    result = client.delete(
        '/product/1',
    )

    assert result.status_code == 200


def test_get_all(db: SQLAlchemy):
    first_product = ProductModel(name="First", price=5.25)
    second_product = ProductModel(name="Second", price=7.50)

    db.session.add(first_product)
    db.session.add(second_product)
    db.session.commit()

    result = ProductList.get()['products']
    assert first_product.name == result[0]['name']
    assert first_product.price == result[0]['price']
    assert second_product.name == result[1]['name']
    assert second_product.price == result[1]['price']


def test_post(client: FlaskClient):
    payload = dict(name='Test', price=8.0)
    client.post(
        '/product-create',
        json=payload
    ).get_json()

    result = client.get('/product/1').get_json()
    assert result['name'] == payload['name']
    assert result['price'] == payload['price']
