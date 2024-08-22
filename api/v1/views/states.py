#!/usr/bin/python3
"""Retrieves a ."""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from flasgger.utils import swag_from


@app_views.route("/states", methods=["GET"], strict_slashes=False)
@swag_from("documentation/state/get_state", methods=['GET'])
def get_all_states():
    """Retrieves all the list of all 'State' objects from storage."""
    states = storage.all(State)
    json_states = [obj.to_dict() for obj in states.values()]
    return jsonify(json_states)


@app_views.route("/states/<string:state_id>",
                 methods=["GET"], strict_slashes=False)
@swag_from("documentation/state/get_id_state.yml", methods=['GET'])
def get_state_by_id(state_id):
    """Retrieves an object with the given id from storage if it exists,
    otherwise raises a 404 error.
    """
    states = storage.all(State)
    id = 'State.' + state_id
    if id not in states.keys():
        abort(404)
    return jsonify(states.get("State." + state_id).to_dict())


@app_views.route("/states/<string:state_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from("documentation/state/delete_state.yml", methods=['DELETE'])
def delete_state_by_id(state_id):
    """Deletes a state by id from the storage if it exists,
    otherwise raises a 404 error.
    """
    states = storage.all(State)
    id = "State." + state_id
    to_del = states.get(id)

    if not to_del:
        abort(404)

    storage.delete(to_del)
    storage.save()

    return make_response(jsonify(dict()), 200)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
@swag_from("documentation/state/post_state.yml", methods=['POST'])
def post_new_state():
    """Creates a new 'State' object."""
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")
    elif "name" not in data.keys():
        abort(400, description="Missing name")
    else:
        state = State(**data)
        state.save()
        return make_response(jsonify(state.to_dict()), 201)


@app_views.route("states/<state_id>", methods=["PUT"], strict_slashes=False)
@swag_from("documentation/state/put_state.yml", methods=['PUT'])
def put_state(state_id):
    """Updates an existing 'State' object if the passed <state_id> is valid,
    otherwise handles error accordingly.
    """
    state = storage.get(State, state_id)
    data = request.get_json(silent=True)

    if not state:
        abort(404)
    elif not data:
        abort(400, description="Not a JSON")
    else:
        data = request.get_json()
        ignore = ['id', 'created_at', 'updated_at']
        [setattr(state, k, v) for k, v in data.items() if k not in ignore]
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
