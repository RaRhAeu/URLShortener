from flask import Blueprint, jsonify, redirect

from urlshortener.api.views.urls import urls_blueprint
from urlshortener.api.views.users import users_blueprint
from urlshortener.database import db
from urlshortener.models import Url

shortcuts_blueprint = Blueprint("shortcuts", "urlshortener")


@shortcuts_blueprint.route('/<short_url>')
def resolve_short_url(short_url):
    url = Url.query(short_url=short_url).first()
    if not url:
        return jsonify(error="url not found"), 404
    url.visits += 1
    db.session.commit()
    return redirect(url.long_url)


def register(app):
    app.register_blueprint(shortcuts_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(urls_blueprint)
