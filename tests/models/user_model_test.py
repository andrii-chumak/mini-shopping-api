from pytest import fixture
from flask_sqlalchemy import SQLAlchemy
from tests.fixtures import app, db
from models.user import UserModel


@fixture
def user() -> UserModel:
    return UserModel(username="TestUser", password='test')


def test_user_create(user: UserModel):
    assert user


def test_user_retrieve(user: UserModel, db: SQLAlchemy):
    db.session.add(user)
    db.session.commit()
    user_res = UserModel.query.first()
    assert user.__dict__ == user_res.__dict__
