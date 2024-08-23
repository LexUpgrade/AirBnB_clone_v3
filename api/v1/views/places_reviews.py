#!/usr/bin/python3
"""Creates view for 'Place' on 'Review' that handles all default RESTful API actions."""
from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request


@app_views.route("/places/<place_id>/reviews",
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Gets the list of all 'Review' objects of a particular
    'Place' object.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [obj.to_dict() for obj in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Gets a specific 'Review' object by <id>."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a specific 'Review' object by <id>."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify(dict()), 200)


@app_views.route("/places/<place_id>/reviews",
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """Creates a new 'Review' object into a specific 'Place' object by <id>."""
    place = storage.get(Place, place_id)
    data = request.get_json(silent=True)
    if not place:
        abort(404)
    elif not data:
        abort(400, description="Not a JSON")
    elif "user_id" not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data.get("user_id"))
    if not user:
        abort(404)
    elif "text" not in data:
        abort(400, description="Missing text")
    else:
        data['place_id'] = place_id
        review = Review(**data)
        review.save()
        return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Updates an existing 'Review' object by <id>."""
    review = storage.get(Review, review_id)
    data = request.get_json(silent=True)
    if not review:
        abort(404)
    elif not data:
        abort(400, description="Not a JSON")
    else:
        ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        [setattr(review, k, v) for k, v in data.items() if k not in ignore]
        return make_response(jsonify(review.to_dict()), 200)
