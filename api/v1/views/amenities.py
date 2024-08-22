#!/usr/bin/python3
"""Creates views for 'Amenity' that handles all default RESTful API actions."""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, make_response, request


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """Gets all 'Amenity' objects from the storage."""
    amenities = storage.all(Amenity)
    if not amenities:
        abort(404)
    data = [value.to_dict() for value in amenities.values()]
    return jsonify(data)


@app_views.route("/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a particular 'Amenity' object from the storage."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    return make_response(jsonify(dict()), 200)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def post_amenity():
    """Create a new instance of 'Amenity' into the storgae."""
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")
    elif "name" not in data:
        abort(400, description="Missing name")
    else:
        amenity = Amenity(**data)
        storage.new(amenity)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("amenities/<amenity_id>",
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Updates properties of a 'Amenity' object in the storage."""
    amenity = storage.get(Amenity, amenity_id)
    data = request.get_json(silent=True)
    if not amenity:
        abort(404)
    elif not data:
        abort(400, description="Not a JSON")
    else:
        ignore = ['id', 'created_at', 'updated_at']
        [setattr(amenity, k, v) for k, v in data.items() if k not in ignore]
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 200)
