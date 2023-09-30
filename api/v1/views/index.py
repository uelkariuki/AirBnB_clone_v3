#!/usr/bin/python3

'''flask blueprint'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """Return a JSON response with status OK."""
    return jsonify({"status": "OK"})
