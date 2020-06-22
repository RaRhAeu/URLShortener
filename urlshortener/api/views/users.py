from flask import Blueprint, jsonify

from urlshortener.models import User
from urlshortener.schemas import UserSchema

users_blueprint = Blueprint("users", "urlshortener", url_prefix="/api")


@users_blueprint.route("/users", strict_slashes=False)
def _list():
    users = User.query().all()
    return jsonify(users=UserSchema().dump(users, many=True))
