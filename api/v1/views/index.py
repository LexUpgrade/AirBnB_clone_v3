#!/usr/bin/python3
"""Creates a 'status' route."""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "City": City, "Place": Place, "Review": Review,
           "State": State, "User": User}


@app_views.route("/status", strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Retrieves the number of each objects by type in the storage."""
    keys = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    response_data = {data[0]: storage.count(data[1])
                     for data in zip(keys, classes.values())}
    return jsonify(**response_data)
