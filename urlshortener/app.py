from flask import Flask

from config import config
from urlshortener.api.cache import cache


class URLShortenerApp(Flask):
    def __init__(self, name="urlshortener", config_name=None, *args, **kwargs):
        super(URLShortenerApp, self).__init__(name, *args, **kwargs)
        self.config.from_object(config[config_name])
        config[config_name].init_app(self)

    def add_sqlalchemy(self):
        from urlshortener.database import db
        db.init_app(self)

    def add_cache(self):
        cache.init_app(self)

    def add_celery(self):
        pass

    def add_logging_handler(self):
        pass

    def register_views(self):
        import urlshortener.api.views
        urlshortener.api.views.register(self)


def create_app(config_name, *args, **kwargs):
    app = URLShortenerApp(config_name=config_name)
    app.add_sqlalchemy()
    app.register_views()
    print(f"APP RUNNING IN {config_name} MODE")
    return app
