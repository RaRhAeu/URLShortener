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
        from urlshortener.worker.celery import celery
        celery.init_app(self)

    def add_logging_handler(self):
        # TODO: change settings
        if self.debug:
            return
        import logging
        from logging import Formatter
        from logging.handlers import RotatingFileHandler

        self.logger.setLevel(logging.INFO)
        path = self.config.get("LOG_FILE")
        if path:
            file_handler = RotatingFileHandler(path, "a", 10000)
            file_handler.setLevel(logging.INFO)

            file_formatter = Formatter(
                "%(asctime)s %(levelname)s: %(message) \
                [in %(pathname)s:%(lineno)d]"
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

    def register_views(self):
        import urlshortener.api.views
        urlshortener.api.views.register(self)


def create_app(config_name, *args, **kwargs):
    app = URLShortenerApp(config_name=config_name)
    app.add_sqlalchemy()
    app.register_views()
    app.add_cache()
    print(f"APP RUNNING IN {config_name} MODE")
    return app
