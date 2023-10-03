#!/usr/bin/python3

"""
New view for Place objects that handles all default RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
""" Importing the required modules"""


@app_views.route('/cities/<city_id>/places/', methods=['GET'])
@app_views.route('/cities/<city_id>/places', methods=['GET'])
def Places_get(city_id):
    """ Function that retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]

    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """ Function that retrieves a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places/', methods=['POST'])
@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    """ Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    if 'user_id' not in request_data:
        abort(400, description="Missing user_id")
    user_id = request_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' not in request_data:
        abort(400, description="Missing name")
    place = Place(name=request_data['name'], city_id=city_id, user_id=user_id)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """ Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending on the JSON
    in the body of the request
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    request_data = request.get_json()
    states = request_data.get('states', [])
    cities = request_data.get('cities', [])
    amenities = request_data.get('amenities', [])

    places = []

    if not any([states, cities, amenities]):
        # if all lists are empty retrieve all Place objects
        places = [place.to_dict() for place in storage.all(Place).values()]
        if not places:
            return jsonify({"error": "No places found"})

    else:
        places = set()

        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.update(city.places)
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.update(city.places)

        if amenities:
            for place in list(places):
                place_amenities = [amenity.id for amenity in place.amenities]
                for amenity_id in amenities:
                    if amenity_id not in place_amenities:
                        places.remove(place)
                        break
        json_places = [place.to_dict() for place in places]
        for json_place in json_places:
            json_place.pop('amenities', None)

        if not json_places:
            return jsonify({"error": "No places found"})

    return jsonify(json_places)
