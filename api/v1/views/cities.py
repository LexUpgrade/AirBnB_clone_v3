#!/usr/bin/python3
"""Creates views for 'City' that handles all default RESTful API actions.
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import abort, jsonify, make_response, request


@app_views.route("/states/<state_id>/cities",
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Gets a list of cities in a particular state."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """Get a city by id."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city_id(city_id):
    """Deletes a particular city from the storage."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify(dict()), 200)


@app_views.route("/states/<state_id>/cities",
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Creates a new 'City'."""
    state = storage.get(State, state_id)
    data = request.get_json(silent=True)

    if not state:
        abort(404)
    elif not data:
        abort(400, description="Not a JSON")
    elif "name" not in data.keys():
        abort(400, description="Missing name")
    else:
        city = City(state_id=state_id, **data)
        city.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route("cities/<city_id>", methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Modifies an existing city by id."""
    city = storage.get(City, city_id)
    data = request.get_json(silent=True)

    if not city:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    [setattr(city, k, v) for k, v in data.items() if k not in ignore]
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
