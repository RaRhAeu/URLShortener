from flask import Blueprint, jsonify
from werkzeug.utils import redirect

from urlshortener.api.cache import cache
from urlshortener.models import Url

shortcuts_blueprint = Blueprint("shortcuts", "urlshortener")


@shortcuts_blueprint.route('/<short_url>')
def resolve_short_url(short_url):
    long_url = cache.get(short_url)
    if not long_url:
        url = Url.query(short_url=short_url).first()
        long_url = url.long_url
        cache.set(short_url, url.long_url, timeout=60)
        if not url:
            return jsonify(error="url not found"), 404
    # TODO: move the logic below to a Celery worker
    # url.visits += 1
    # db.session.commit()
    return redirect(long_url)
