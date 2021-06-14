from pytest import fixture
from flask_sqlalchemy import SQLAlchemy
from flask.testing import FlaskClient
from tests.fixtures import app, db, client, user_token


@fixture()
def user_with_filled_cart_token(db: SQLAlchemy, client: FlaskClient, user_token: str):
    payload = dict(name="Test", price=5.25)
    product = client.post(
        '/product-create',
        json=payload
    ).get_json()

    client.post('/cart',
                headers={'Authorization': 'JWT ' + user_token},
                json={'product_id': product['id']}
                )

    return user_token


def test_create(client: FlaskClient, user_with_filled_cart_token: str):

    order = client.post('/create-order', headers={'Authorization': 'JWT ' + user_with_filled_cart_token}).get_json()

    assert order
    assert len(order['products']) == 1


def test_get(client: FlaskClient, user_with_filled_cart_token: str):
    order = client.post('/create-order', headers={'Authorization': 'JWT ' + user_with_filled_cart_token}).get_json()

    order_res = client.get('/order/{}'.format(order['id']),
                           headers={'Authorization': 'JWT ' + user_with_filled_cart_token}
                           ).get_json()
    print(order_res)
    assert order_res['total'] == order['total']


def test_total(client: FlaskClient, user_token: str):
    payload = dict(name="Test", price=25.0)
    product = client.post(
        '/product-create',
        json=payload
    ).get_json()

    for _ in range(4):
        client.post('/cart',
                    headers={'Authorization': 'JWT ' + user_token},
                    json={'product_id': product['id']}
                    )

    order = client.post('/create-order', headers={'Authorization': 'JWT ' + user_token}).get_json()
    assert order['total'] == 99.0
