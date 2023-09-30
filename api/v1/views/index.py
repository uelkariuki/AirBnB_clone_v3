#!/usr/bin/python3

'''flask blueprint'''
from api.v1.views import app_views
from flask import jsonify
from models import storage
import json

""" Importing the required modules"""


@app_views.route('/status', methods=['GET'])
def status():
    """Return a JSON response with status OK."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Create an endpoint that retrieves the number of each objects by type
    """
    number_of_objects = storage.count()
    result = json.dumps(number_of_objects, indent=4)
    return result
