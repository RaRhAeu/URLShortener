from urlshortener.api.views.shortcuts import shortcuts_blueprint
from urlshortener.api.views.urls import urls_blueprint
from urlshortener.api.views.users import users_blueprint


def register(app):
    # TODO: add cors here
    app.register_blueprint(shortcuts_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(urls_blueprint)
