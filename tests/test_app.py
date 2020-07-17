from urlshortener.app import URLShortenerApp


# TODO: test app methods, add_cache etc...
def test_app_instance(app):
    assert isinstance(app, URLShortenerApp)
