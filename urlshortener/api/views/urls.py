from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from urlshortener.database import db
from urlshortener.models import Url
from urlshortener.schemas import UrlSchema

urls_blueprint = Blueprint("urls", "urlshortener", url_prefix="/api")


@urls_blueprint.route("/urls", strict_slashes=False)
def _list():
    urls = Url.query().order_by("created")
    return jsonify(urls=UrlSchema().dump(urls, many=True))


@urls_blueprint.route("/urls/<url_id>")
def read(url_id):
    url = Url.get(url_id)
    url.visits += 1
    db.session.commit()
    return jsonify(UrlSchema().dump(url))


@urls_blueprint.route("/urls", methods=["POST"])
def create_url():
    json = request.get_json()
    try:
        data = UrlSchema().load(json)
    except ValidationError as e:
        return jsonify(error="validation failed", fields=e.messages), 422

    if data.get("short_url"):
        if Url.exists(short_url=data["short_url"]):
            return jsonify(error="duplicate url"), 422

    url = Url(**data)
    url.short_url = data.get("short_url")
    db.session.add(url)
    db.session.commit()
    return jsonify(UrlSchema().dump(url))


@urls_blueprint.route("/urls/<url_id>", methods=["DELETE"])
def delete(url_id):
    url = Url.get(url_id)
    if url:
        db.session.delete(url)
        db.session.commit()
        return jsonify(url.id), 200
