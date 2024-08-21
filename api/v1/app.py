#!/usr/bin/python3
"""Starts a RESTful API application."""
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Closes the current storage session."""
    storage.close()


@app.errorhandler(404)
def errorhandler(error):
    """A 404 errorhandler."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)
