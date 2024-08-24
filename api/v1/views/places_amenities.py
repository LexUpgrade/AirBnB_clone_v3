#!/usr/bin/python3
"""Creates views for 'Amenity' on 'Place' that handles all
default RESTful API actions.
"""
from os import getenv
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


@app_views.route("/places/<place_id>/amenities",
                 methods=['GET'], strict_slashes=False)
def get_amenity(place_id):
    """Gets a list of all 'Amenity' object for a specific 'Place' object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        if getenv('HBNB_TYPE_STORAGE') == "db":
            amenities = [aminity.to_dict() for amenity in place.amenities]
        else:
            amenities = [storage.get(Amenity, amenity_id).to_dict()
                         for amenity_id in place.amenity_ids]
        return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_amenities(place_id, amenity_id):
    """Deletea a particular 'Amenity' object from a particular 'Place'
    object.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        aborot(404)
    if getenv('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    place.save()
    return make_response(jsonify(dict()), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['POST'], strict_slashes=False)
def post_new_amenity(place_id, amenity_id):
    """Creates a new 'Amenity' object for a specific 'Place' object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == "db":
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity.append(amenity)
    else:
        if amenity in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
