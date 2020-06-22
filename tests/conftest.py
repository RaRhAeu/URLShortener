import pytest

from tests import clean_db, setup_db, teardown_db
from urlshortener import create_app, database
from urlshortener.app import URLShortenerApp


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
