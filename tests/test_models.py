import pytest

from urlshortener.models import User
from tests import data


def test_user_create_delete(db_session):
    user = data.example_user()
    db_session.add(user)
    db_session.commit()
    user_id = user.id
    assert user_id is not None

    assert db_session.query(User).get(user_id) is not None

    db_session.delete(user)
    db_session.commit()

    assert db_session.query(User).get(user_id) is None


def test_user_repr_is_str(db_session):
    john = data.john()
    db_session.add(john)
    db_session.commit()
    assert isinstance(repr(john), str)
    assert repr(john) == "<User: John Doe>"


def test_hash_password():
    u_hash = User._hash_password("secret123", salt=b"abcdef")
    assert (
        u_hash == "bef57ec7f53a6d40beb640a780a639c83bc29ac8a9816f1fc6c5c6dcd93c47212"
                  "72b82aa344691fb4037f20617b1d19212042e7e6cb39f4ba0dad95d8137104a"
    )
    assert isinstance(u_hash, str)


def test_verify_password():
    john = data.john()
    assert john.verify_password("jane123") is True
    assert john.verify_password("jane12") is False


def test_user_permissions(db_session):
    admin = data.example_admin()
    user = data.example_user()
    db_session.add(admin)
    db_session.add(user)
    db_session.commit()
    assert admin.is_manager() is True
    assert user.is_manager() is False
    # is user readable by himself? (Yes)
    assert user.is_readable(user) is True
    # is user readable by admin? (Yes)
    assert user.is_readable(admin) is True
    # is admin readable by admin? (Yes)
    assert admin.is_readable(admin) is True
    # is admin readable by user? (No)
    assert admin.is_readable(user) is False


def test_user_find_by_credentials(db_session):
    user = data.example_user()
    db_session.add(user)
    db_session.commit()
    assert user is User.by_credentials(email="example@email.com", password="test")


def test_url_repr(db_session):
    url = data.example_url()
    db_session.add(url)
    db_session.commit()
    url_id = url.id
    short_url = url.short_url
    assert isinstance(repr(url), str)
    assert repr(url) == f"<Url {url_id}: {short_url}>"
