#!/usr/bin/python3

'''handle all default RESTFul API actions for User objects'''
from flask import abort, jsonify, request
from models.city import City
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404, "Not found")
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404, "Not found")
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404, "Not found")
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    keys_to_ignore = ["id", "email", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in keys_to_ignore:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
