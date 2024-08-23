#!/usr/bin/python3
"""Creates routes for 'Place' that handles all default RESTful API actions."""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


@app_views.route("/cities/<city_id>/places",
                 methods=['GET'], strict_slashes=False)
def get_place_city(city_id):
    """Gets the list of 'Place' objects of a 'City' object by <city_id>."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = list()
    [places.append(obj.to_dict()) for obj in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Gets a particular 'Place' object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a specific 'Place' object from the storage."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify(dict()), 200)


@app_views.route("/cities/<city_id>/places",
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Creates a new 'Place' object into an existing 'City' object."""
    city = storage.get(City, city_id)
    data = request.get_json(silent=True)
    if not city:
        abort(404)
    elif not data:
        abort(400, description="Not a JSON")
    elif "user_id" not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data.get('user_id'))
    if not user:
        abort(404)
    elif "name" not in data:
        abort(400, description="Missing name")
    else:
        place = Place(**data)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates properties of a 'Place' object in the storage."""
    place = storage.get(Place, place_id)
    data = request.get_json(silent=True)
    if not place:
        abort(404)
    elif not data:
        abort(400, description="Not a JSON")
    else:
        ignore = ['id', 'user_id', 'city_id', 'craeted_at', 'updated_at']
        [setattr(place, k, v) for k, v in data.items if k not in ignore]
        place.save()
        return make_response(jsonify(place.to_dict()), 200)
