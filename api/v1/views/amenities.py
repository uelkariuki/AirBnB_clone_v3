#!/usr/bin/python3

"""
New view for Amenity objects that handles all default RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
""" Importing the required modules"""


@app_views.route('/amenities/', methods=['GET'])
@app_views.route('/amenities', methods=['GET'])
def amenities_get():
    """ Function that retrieves the list of all Amenity objects"""
    amenities = [amenity.to_dict() for amenity in
                 storage.all(Amenity).values()]

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """ Function that retrieves an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Deletes an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
@app_views.route('/amenities', methods=['POST'])
def post_amenity():
    """ Creates an Amenity"""
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    if 'name' not in request_data:
        abort(400, description="Missing name")
    amenity = Amenity(name=request_data['name'])
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    """ Updates an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
