from flask import (Blueprint, jsonify, make_response, request, send_file,
                   url_for)
from marshmallow import ValidationError
from sqlalchemy import desc

from urlshortener.database import db
from urlshortener.models import Url
from urlshortener.schemas import UrlSchema
from urlshortener.utils import generate_qr_code

urls_blueprint = Blueprint("urls", "urlshortener", url_prefix="/api")


@urls_blueprint.route("/urls", strict_slashes=False)
def _list():
    urls = Url.query().order_by(desc("created"))
    return jsonify(urls=UrlSchema().dump(urls, many=True))


@urls_blueprint.route("/urls/<int:url_id>")
def read(url_id):
    url = Url.get(url_id)
    if not url:
        return jsonify(error="object not found"), 404
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


@urls_blueprint.route("/urls/<int:url_id>", methods=["DELETE"])
def delete(url_id):
    url = Url.get(url_id)
    if not url:
        return jsonify(error="object not found"), 404
    db.session.delete(url)
    db.session.commit()
    return jsonify(url.id), 200


@urls_blueprint.route("/urls/<url_id>/get_qr", methods=["GET"])
def get_qr_code(url_id):
    """Generates QR Code for the given url_id,
    if request parameter direct is set to 'true',
    then generates QR directly for desired url,
    otherwise, uses shortcuts.redirect
    """
    url = Url.get(url_id)
    if not url:
        return jsonify(error="object not found"), 404
    if request.args.get("direct") == "true":
        data = url.long_url
    else:
        data = url_for(
            'shortcuts.redirect_short_url',
            short_url=url.short_url,
            _external=True
        )
    qr = generate_qr_code(data)
    response = make_response(send_file(qr, mimetype="image/png"))
    # response.headers['Content-Transfer-Encoding'] = 'base64'
    return response
