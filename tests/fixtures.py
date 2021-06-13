import pytest

from app import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def db(app):
    from database import db

    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()
