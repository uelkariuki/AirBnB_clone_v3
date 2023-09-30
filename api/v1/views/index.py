#!/usr/bin/python3

"""Flask blueprint"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
import json
""" Importing required modules"""


@app_views.route('/status', methods=['GET'])
def status():
    """Return a JSON response with status OK."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Create an endpoint that retrieves the number of each objects by type
    """
    number_of_objects = storage.count(by_type=True)
    return jsonify(number_of_objects)
