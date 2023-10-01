#!/usr/bin/python3

'''handle all default RESTFul API actions for Review objects'''
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404, "Not found")
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404, "Not found")
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404, "Not found")
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404, "Not found")
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404, "User not found")
    if "text" not in data:
        abort(400, "Missing text")
    new_review = Review(**data)
    new_review.place_id = place.id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404, "Not found")
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    keys_to_ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in keys_to_ignore:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
