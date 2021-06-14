import pytest

from flask.testing import FlaskClient
from app import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    from database import db

    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()


@pytest.fixture
def user_token(client: FlaskClient):
    payload = dict(username='new_user', password='new_user')

    client.post(
        '/register',
        json=payload
    )

    token = client.post(
        '/auth',
        json=payload
    ).get_json()['access_token']

    return token
