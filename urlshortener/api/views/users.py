from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from urlshortener.database import db
from urlshortener.models import User
from urlshortener.schemas import UserSchema

users_blueprint = Blueprint("users", "urlshortener", url_prefix="/api")


@users_blueprint.route("/users", methods=['GET'], strict_slashes=False)
def _list():
    users = User.query().all()
    return jsonify(users=UserSchema().dump(users, many=True))


@users_blueprint.route("/users/<int:user_id>", methods=['GET'])
def read(user_id):
    # TODO: add user.is_self or user.is_manager
    user = User.get(user_id)
    if not user:
        return jsonify(error="user not found"), 404
    return jsonify(user=UserSchema().dump(user))


@users_blueprint.route("/users", methods=['POST'])
def create():
    json = request.get_json()
    try:
        data = UserSchema().load(json)
    except ValidationError as e:
        return jsonify(error="validation failed", fields=e.messages), 422
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(UserSchema().dump(user))
