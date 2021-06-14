from flask_sqlalchemy import SQLAlchemy
from flask.testing import FlaskClient
from tests.fixtures import app, db, client
from models.user import UserModel
from resources.user import User


def test_get(db: SQLAlchemy):
    user = UserModel(username="TestUser", password='test1234')

    db.session.add(user)
    db.session.commit()

    result = User.get(1)

    assert result['username'] == user.username


def test_delete(db: SQLAlchemy, client: FlaskClient):
    user = UserModel(username="TestUser2", password='test')

    db.session.add(user)
    db.session.commit()

    result = client.delete(
        '/user/1',
    )

    assert result.status_code == 200

    result = client.delete(
        '/user/1',
    )

    assert result.status_code == 404


def test_register(client: FlaskClient):
    payload = dict(username='new_user', password='new_user')
    client.post(
        '/register',
        json=payload
    ).get_json()

    result = client.get('/user/1').get_json()
    assert result['username'] == payload['username']

    result = client.post(
        '/register',
        json=payload
    )

    assert result.status_code == 400
