from faker import Faker
from urlshortener.models import User, Url


def example_user():
    u1 = User()
    u1.first_name = "Example"
    u1.last_name = "User"
    u1.email_address = "example@email.com"
    u1.password = "test"
    return u1


def example_admin():
    admin = User()
    admin.first_name = "Example"
    admin.last_name = "Admin"
    admin.email_address = "example_admin@email.com"
    admin.password = "password"
    admin.admin = True
    return admin


def john():
    user = User(first_name="John", last_name="Doe", email_address=u"johnny@doe.com")
    user.original_password = user.password = "jane123"
    return user


def example_url():
    url = Url()
    url.long_url = "https://www.google.com/"
    return url