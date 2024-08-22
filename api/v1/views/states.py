#!/usr/bin/python3
"""Retrieves a ."""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """Retrieves all the list of all 'State' objects from storage."""
    states = storage.all(State)
    json_states = [obj.to_dict() for obj in states.values()]
    return jsonify(json_states)


@app_views.route("/states/<string:state_id>",
                 methods=["GET"], strict_slashes=False)
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
def post_new_state():
    """Creates a new 'State' object."""
    new_args = request.get_json()
    if type(new_args) is not dict:
        abort(400, description="Not a JSON")
    elif "name" not in new_args.keys():
        abort(404, description="Missing name")
    else:
        new_state = State(**new_args)
        storage.new(new_state)
        storage.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("states/<state_id>", methods=["PUT"], strict_slashes=False)
def put_state_obj(state_id):
    """Updates an existing 'State' object if the passed <state_id> is valid,
    otherwise handles error accordingly.
    """
    states = storage.all(State)
    id = "State." + state_id

    if id not in states.keys():
        abort(404)

    json_body = request.get_json()
    if type(json_body) is not dict:
        abort(400, description="Not a JSON")
    else:
        state_to_mod = states.get(id)
        ignore = ['id', 'created_at', 'updated_at']
        [setattr(state_to_mod, k, v) for k, v in json_body.items()
            if k not in ignore]
        storage.save()
        return make_response(jsonify(state_to_mod.to_dict()), 200)
