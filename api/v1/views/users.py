#!/usr/bin/python3
"""Creates routes for 'User' that handdle all default RESTful API actions."""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, make_response, request


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """Gets a list of all 'User' objects from storage."""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route("users/<user_id>",
                 methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """Gets a specific user from the storage."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("users/<user_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_user_id(user_id):
    """Deletes a 'User' object by an id."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify(dict()), 200)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a new 'User' object."""
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")
    elif 'email' not in data:
        abort(400, description="Missing email")
    elif 'password' not in data:
        abort(400, description="Missing password")
    else:
        user = User(**data)
        storage.new(user)
        storage.save()
        return make_response(user.to_dict(), 201)


@app_views.route("/users/<user_id>",
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates an existing 'User' object, otherwise handle errors
    accordingly.
    """
    user = storage.get(User, user_id)
    data = request.get_json(silent=True)
    if not user:
        abort(404)
    elif not data:
        abort(400, description="Not a JSON")
    else:
        ignore = ['id', 'craeted_at', 'updated_at']
        [setattr(user, k, v) for k, v in data.items() if k not in ignore]
        user.save()
        return make_response(jsonify(user.to_dict()), 200)
