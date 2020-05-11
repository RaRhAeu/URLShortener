from faker import Faker
from urlshortener.models import User, Url


def example_user():
    u1 = User()
    u1.first_name = "Example"
    u1.last_name = "User"
    u1.email_address = "example@email.com"
    u1.password = "test"
    return u1


def john():
    user = User(first_name=u"John", last_name=u"Doe", email_address=u"johnny@doe.com")
    user.original_password = user.password = u"jane123"
    return user


def example_url():
    url = Url()
    url.long_url = "https://www.google.com/"
    return url