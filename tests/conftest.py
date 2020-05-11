import pytest
from urlshortener import create_app
from urlshortener.app import URLShortenerApp
from urlshortener import database
from tests import setup_db, teardown_db, clean_db


@pytest.fixture(scope="session")
def app():
    """ Global application fixture"""
    yield create_app(config_name="testing")


@pytest.fixture(scope="session")
def db(app):
    """ Creates clean database schema and drops it on teardown"""
    assert isinstance(app, URLShortenerApp)
    setup_db(app)
    yield database.db
    teardown_db()


@pytest.fixture(scope="function")
def db_session(db, app):
    """Provides clean database before each test"""
    assert isinstance(app, URLShortenerApp)
    with app.app_context():
        clean_db()
        yield db.session
        db.session.rollback()
