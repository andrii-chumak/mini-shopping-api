from pytest import fixture
from flask_sqlalchemy import SQLAlchemy
from flask.testing import FlaskClient
from tests.fixtures import app, db, client, user_token


@fixture()
def product(db: SQLAlchemy, client: FlaskClient):
    payload = dict(name="Test", price=5.25)
    product = client.post(
        '/product-create',
        json=payload
    ).get_json()

    return product


def test_get(client: FlaskClient, user_token: str):

    cart = client.get('/cart', headers={'Authorization': 'JWT ' + user_token})

    assert cart


def test_post(client: FlaskClient, user_token: str, product: dict):

    result = client.post('/cart',
                         headers={'Authorization': 'JWT ' + user_token},
                         json={'product_id': product['id']}
                         ).get_json()['products'][0]

    assert result['name'] == product['name']
    assert result['price'] == product['price']


def test_get_total(client: FlaskClient, user_token: str, product: dict):

    client.post('/cart',
                headers={'Authorization': 'JWT ' + user_token},
                json={'product_id': product['id']}
                )

    client.post('/cart',
                headers={'Authorization': 'JWT ' + user_token},
                json={'product_id': product['id']}
                )

    result = client.get('/cart-total', headers={'Authorization': 'JWT ' + user_token}).get_json()

    assert result['subtotal'] == product['price'] * 2
